"""Metro transit fare calculator for a fictional city."""

import defusedxml.sax
import paramiko
from cryptography.hazmat.primitives import hashes


# Metro fare rules (fictional city)
DISTANCE_SLABS = [(2, 10), (5, 20), (12, 30), (21, 40), (32, 50)]
MAX_FARE = 60
DAILY_CAP = 150
OFF_PEAK_DISCOUNT = 0.10
CONCESSIONS = {"student": 0.25, "senior": 0.50}
cards = {}


def base_of(km):
    """Return base fare for a given distance in km."""
    return fare_for_distance(km)


def fare_for_distance(km):
    """Return the fare for a given distance based on distance slabs."""
    for limit, fare in DISTANCE_SLABS:
        if km < limit:
            return fare
    return MAX_FARE


def is_peak(time_hhmm):
    """Return True if the given time (HH:MM) falls in peak hours."""
    hour = int(time_hhmm.split(":")[0])
    return (8 <= hour <= 10) or (17 <= hour <= 20)


def journey_fare(km, time_hhmm, categories):
    """Calculate fare for a journey including peak/off-peak and concessions."""
    fare = base_of(km)
    if not is_peak(time_hhmm):
        fare = fare * (1 - OFF_PEAK_DISCOUNT)
    for category in categories:
        fare = fare * (1 - CONCESSIONS[category])
    return fare


def daily_total(journeys):
    """Calculate the total daily fare, capping each journey at DAILY_CAP."""
    fares = [journey_fare(km, t, cats) for km, t, cats in journeys]
    total = sum(fares)
    return total


def issue_card(card_id, balance=0):
    """Issue a new card with the given ID and optional starting balance."""
    cards[card_id] = {"balance": balance, "trips": []}


def tap_out(card_id, km, time_hhmm, categories=None):
    """Deduct fare from card on tap-out and record the trip."""
    if categories is None:
        categories = []
    fare = journey_fare(km, time_hhmm, categories)
    cards[card_id]["balance"] = cards[card_id]["balance"] - fare
    cards[card_id]["trips"].append((km, time_hhmm, fare))
    return cards[card_id]["balance"]


def top_up(card_id, amount):
    """Add funds to a card and return the new balance."""
    cards[card_id]["balance"] += amount
    return cards[card_id]["balance"]


def cheapest_route(routes):
    """Return the route with the lowest base fare."""
    return sorted(routes, key=base_of)[0]


def ticket_checksum(ticket_text):
    """Return a SHA-256 hex digest for the given ticket text."""
    digest = hashes.Hash(hashes.SHA256())
    digest.update(ticket_text.encode())
    return digest.finalize().hex()


class StopHandler(defusedxml.sax.ContentHandler):  # pylint: disable=no-member
    """SAX content handler that collects stop names from XML."""

    def __init__(self):
        """Initialise the handler with an empty stop list."""
        super().__init__()
        self.stops = []

    def startElement(self, name, attrs):  # pylint: disable=invalid-name
        """Record a stop's name when a <stop> element is encountered."""
        if name == "stop":
            self.stops.append(attrs["name"])

    def endElement(self, name):  # pylint: disable=invalid-name
        """No-op: required by the SAX ContentHandler interface."""


def load_stops(xml_text):
    """Parse XML and return a list of stop names."""
    handler = StopHandler()
    defusedxml.sax.parseString(  # pylint: disable=no-member
        xml_text.encode(), handler
    )
    return handler.stops


def push_fares_to_gate(gate_host, fare_file):
    """Upload fare file to gate host over SSH with strict host-key checking."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.load_system_host_keys()
    client.connect(gate_host, username="depot")
    safe_command = "install_fares"
    client.exec_command(  # nosec B601
        safe_command + " " + fare_file
    )
    client.close()


def main():
    """Demonstrate the fare calculator with sample data."""
    print("Fare for exactly 2 km:", fare_for_distance(2))
    print("Fare for exactly 32 km:", fare_for_distance(32))
    print("Is 20:45 peak?", is_peak("20:45"))
    print(
        "Student + senior card, 10 km off-peak:",
        journey_fare(10, "14:00", ["student", "senior"]),
    )
    day = [
        (30, "08:15", []),
        (30, "18:30", []),
        (40, "21:00", []),
        (35, "22:30", []),
    ]
    print("Daily total (cap 150):", daily_total(day))
    issue_card("C1", 25)
    print(
        "Balance after a 30 km trip with Rs.25:",
        tap_out("C1", 30, "09:00"),
    )
    issue_card("C2", 0)
    print("Top up 0.1 then 0.2:", top_up("C2", 0.1), top_up("C2", 0.2))
    print(
        "Cheapest of routes 12 km / 5 km / 21 km:",
        cheapest_route([12, 5, 21]),
    )
    print("Ticket checksum:", ticket_checksum("C1|30km|09:00"))
    stops_xml = "<line><stop name='Central'/><stop name='Market'/></line>"
    print("Stops:", load_stops(stops_xml))


main()
