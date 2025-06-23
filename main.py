from models.ticket import Ticket, TicketAnalysis
from agents.priority_assessor import PriorityAssessor
from agents.sentiment_analyzer import SentimentAnalyzer
from agents.routing_specialist import RoutingSpecialist
from dotenv import load_dotenv

load_dotenv()


class TicketAnalyzer:
    def __init__(self):
        self.priority_assessor = PriorityAssessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.routing_specialist = RoutingSpecialist()

    def analyze_ticket(self, ticket_data: dict) -> TicketAnalysis:
        ticket = Ticket(**ticket_data)

        priority = self.priority_assessor.assess(ticket)
        sentiment = self.sentiment_analyzer.analyze(ticket.message)
        routing = self.routing_specialist.route(
            ticket.model_dump(),  # Changed from dict() to model_dump()
            priority.level,
            sentiment
        )

        return TicketAnalysis(
            ticket_id=ticket.ticket_id,
            priority=priority.model_dump(),  # Serialize the priority object
            routing=routing.model_dump(),  # Serialize the routing object
            combined_notes=self._check_conflicts(priority, routing)
        )

    def _check_conflicts(self, priority, routing):
        if priority.level == "critical" and routing.department != "security":
            return "Critical issue not routed to security"
        return None


if __name__ == "__main__":
    analyzer = TicketAnalyzer()

    from tests.test_cases import test_tickets as test_cases

    for case in test_cases:
        result = analyzer.analyze_ticket(case)
        print(f"\nTicket {result.ticket_id}:")
        print(f"  Priority: {result.priority['level']} ({result.priority['rationale']})")
        print(f"  Department: {result.routing['department']}")
        print(f"  Response Time: {result.routing['expected_response_time']}")
        if result.combined_notes:
            print(f"  Note: {result.combined_notes}")