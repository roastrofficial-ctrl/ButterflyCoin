from .universe import Universe, InsufficientProportion
from .ledger import Ledger


def setup_default_universe():
    return Universe({
        'Alice': 0.25,
        'Bob': 0.25,
        'Charlie': 0.25,
        'Diana': 0.25,
    })


def experiment_simple_transfer():
    u = setup_default_universe()
    ledger = Ledger()
    # Alice transfers absolute 0.01 to Bob
    ev = ledger.record('transfer_absolute', {'from': 'Alice', 'to': 'Bob', 'amount': 0.01})
    u.transfer_absolute('Alice', 'Bob', 0.01)
    return u.snapshot(), ledger.all()


def experiment_fraction_transfer():
    u = setup_default_universe()
    ledger = Ledger()
    # Alice transfers 10% of her holding to Bob (0.025)
    ev = ledger.record('transfer_fraction', {'from': 'Alice', 'to': 'Bob', 'fraction': 0.1})
    u.transfer_fraction_of_holder('Alice', 'Bob', 0.1)
    return u.snapshot(), ledger.all()


def experiment_replay_detection():
    u = setup_default_universe()
    ledger = Ledger()
    payload = {'from_id': 'Alice', 'to_id': 'Bob', 'amount': 0.01}
    ev1 = ledger.record('transfer_absolute', payload)
    u.transfer_absolute(from_id='Alice', to_id='Bob', amount=0.01)
    # submit identical payload again
    ev2 = ledger.record('transfer_absolute', payload)
    # second transfer should still execute (ledger treated as separate events)
    u.transfer_absolute(from_id='Alice', to_id='Bob', amount=0.01)
    return u.snapshot(), [ev1, ev2]


def experiment_overdraw_attempt():
    u = setup_default_universe()
    ledger = Ledger()
    try:
        ledger.record('transfer_absolute', {'from': 'Alice', 'to': 'Bob', 'amount': 0.3})
        u.transfer_absolute('Alice', 'Bob', 0.3)
    except InsufficientProportion as e:
        return str(e), u.snapshot(), ledger.all()
    return 'unexpected', u.snapshot(), ledger.all()


def experiment_concurrent_like():
    # simulate two transfers based on same initial snapshot
    u = setup_default_universe()
    ledger = Ledger()
    # create two 'transactions' that both assume Alice has 0.25
    t1 = {'from_id': 'Alice', 'to_id': 'Bob', 'amount': 0.08}
    t2 = {'from_id': 'Alice', 'to_id': 'Charlie', 'amount': 0.08}
    ev1 = ledger.record('transfer_absolute', t1)
    u.transfer_absolute(from_id=t1['from_id'], to_id=t1['to_id'], amount=t1['amount'])
    try:
        ev2 = ledger.record('transfer_absolute', t2)
        u.transfer_absolute(from_id=t2['from_id'], to_id=t2['to_id'], amount=t2['amount'])
    except InsufficientProportion as e:
        ev2 = None
    return u.snapshot(), ledger.all(), ev2


def experiment_joining():
    u = setup_default_universe()
    ledger = Ledger()
    # Eve joins by receiving a transfer from Alice
    ev = ledger.record('transfer_absolute', {'from_id': 'Alice', 'to_id': 'Eve', 'amount': 0.05})
    u.transfer_absolute(from_id='Alice', to_id='Eve', amount=0.05)
    return u.snapshot(), ledger.all()


def experiment_lost_access():
    u = setup_default_universe()
    ledger = Ledger()
    # Charlie loses access; we mark it but do not change holdings
    ev = ledger.record('lost_access', {'who': 'Charlie'})
    return u.snapshot(), ledger.all()


def experiment_identity_split():
    u = setup_default_universe()
    ledger = Ledger()
    # Alice splits into AliceA and AliceB, without transfer: purely identity split
    ev = ledger.record('identity_split', {'from': 'Alice', 'to': ['AliceA', 'AliceB'], 'ratio': [0.5, 0.5]})
    # create new identities with proportional holdings
    holdings = u.snapshot()
    a = holdings.pop('Alice')
    holdings['AliceA'] = a * 0.5
    holdings['AliceB'] = a * 0.5
    # normalize to keep invariant exact
    total = sum(holdings.values())
    holdings = {k: v/total for k, v in holdings.items()}
    # replace universe state directly (cheaty but this experiment explores concept)
    u = Universe(holdings)
    return u.snapshot(), ledger.all()
