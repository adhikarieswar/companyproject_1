from pydantic import BaseModel
from typing import Optional, Dict, Any

class PriorityAssessment(BaseModel):
    level: str  # "low", "medium", "high", "critical"
    rationale: str

class RoutingRecommendation(BaseModel):
    department: str
    expected_response_time: str

class Ticket(BaseModel):
    ticket_id: str
    customer_tier: str
    subject: str
    message: str
    previous_tickets: int
    monthly_revenue: float
    account_age_days: int

class TicketAnalysis(BaseModel):
    ticket_id: str
    priority: Dict[str, Any]  # Now accepts serialized PriorityAssessment
    routing: Dict[str, Any]   # Now accepts serialized RoutingRecommendation
    combined_notes: Optional[str] = None