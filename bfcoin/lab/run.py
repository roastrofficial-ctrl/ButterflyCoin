from .experiments import *


def run_all():
    results = {}
    results['simple_transfer'] = experiment_simple_transfer()
    results['fraction_transfer'] = experiment_fraction_transfer()
    results['replay'] = experiment_replay_detection()
    results['overdraw'] = experiment_overdraw_attempt()
    results['concurrent'] = experiment_concurrent_like()
    results['joining'] = experiment_joining()
    results['lost_access'] = experiment_lost_access()
    results['identity_split'] = experiment_identity_split()
    return results


if __name__ == '__main__':
    import json
    res = run_all()
    # Recursively serialize Event-like objects (and lists/tuples/dicts)
    def serialize(obj):
        if hasattr(obj, 'id') and hasattr(obj, 'kind') and hasattr(obj, 'details'):
            return {'id': obj.id, 'kind': obj.kind, 'details': obj.details}
        if isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [serialize(v) for v in obj]
        return obj

    serial = {k: serialize(v) for k, v in res.items()}
    print(json.dumps(serial, indent=2))
