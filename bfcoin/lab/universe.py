from dataclasses import dataclass, replace
from typing import Dict, Tuple, List
import copy


class InsufficientProportion(Exception):
    pass


@dataclass(frozen=True)
class State:
    holdings: Dict[str, float]

    def total(self) -> float:
        return sum(self.holdings.values())


class Universe:
    """Immutable-size monetary universe. Holdings are proportions summing to 1.0.

    Representation: internal holdings are Python floats but normalized to avoid
    drift. All operations return new State objects (functional style) and the
    conservation invariant is strictly enforced.
    """

    def __init__(self, initial: Dict[str, float]):
        s = sum(initial.values())
        if abs(s - 1.0) > 1e-12:
            raise ValueError("Initial holdings must sum to 1.0")
        self._state = State(holdings=dict(initial))

    def state(self) -> State:
        return copy.deepcopy(self._state)

    def _normalize(self, holdings: Dict[str, float]) -> Dict[str, float]:
        total = sum(holdings.values())
        if total == 0:
            return holdings
        # normalize to exactly 1.0
        return {k: v / total for k, v in holdings.items()}

    def transfer_absolute(self, from_id: str, to_id: str, amount: float) -> State:
        """Transfer an absolute proportion `amount` of U from from_id to to_id.

        Fails if `from_id` doesn't have at least `amount`.
        """
        holdings = dict(self._state.holdings)
        if from_id not in holdings:
            raise KeyError(from_id)
        if to_id not in holdings:
            # joining a new participant is allowed; create with zero then transfer
            holdings[to_id] = 0.0
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if holdings[from_id] + 1e-15 < amount:
            raise InsufficientProportion(f"{from_id} has {holdings[from_id]}, needs {amount}")
        holdings[from_id] -= amount
        holdings[to_id] += amount
        holdings = self._normalize(holdings)
        # enforce exact conservation
        if abs(sum(holdings.values()) - 1.0) > 1e-12:
            raise AssertionError("Universe invariant broken")
        new_state = State(holdings=holdings)
        self._state = new_state
        return new_state

    def transfer_fraction_of_holder(self, from_id: str, to_id: str, fraction: float) -> State:
        """Transfer `fraction` of `from_id`'s current holding to `to_id`.

        Example: if Alice has 0.25 and fraction=0.1, transfer 0.025.
        """
        holdings = dict(self._state.holdings)
        if from_id not in holdings:
            raise KeyError(from_id)
        if to_id not in holdings:
            holdings[to_id] = 0.0
        if fraction < 0 or fraction > 1:
            raise ValueError("fraction must be in [0,1]")
        amount = holdings[from_id] * fraction
        return self.transfer_absolute(from_id, to_id, amount)

    def snapshot(self) -> Dict[str, float]:
        return dict(self._state.holdings)

    def total(self) -> float:
        return sum(self._state.holdings.values())
