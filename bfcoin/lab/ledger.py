from dataclasses import dataclass
from typing import List, Dict, Any
import hashlib


@dataclass
class Event:
    id: str
    kind: str
    details: Dict[str, Any]


class Ledger:
    """A simple append-only ledger recording events and producing deterministic IDs.

    This is not a distributed ledger; it's an ordered journal used to test replay,
    duplication, and reconstruction questions.
    """

    def __init__(self):
        self.events: List[Event] = []

    def record(self, kind: str, details: Dict[str, Any]) -> Event:
        payload = f"{kind}:{sorted(details.items())}"
        eid = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        # if same payload appears twice, append a counter to distinguish
        counter = 1
        base_eid = eid
        while any(e.id == eid for e in self.events):
            counter += 1
            eid = f"{base_eid}-{counter}"
        ev = Event(id=eid, kind=kind, details=details)
        self.events.append(ev)
        return ev

    def find(self, eid: str):
        for e in self.events:
            if e.id == eid:
                return e
        return None

    def all(self) -> List[Event]:
        return list(self.events)
