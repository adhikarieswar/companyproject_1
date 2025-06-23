📄 Ticket Analyzer Documentation
Overview:
The Ticket Analyzer System leverages large language models (LLMs), natural language processing (NLP), and rule-based logic to intelligently assess and route customer support tickets. The system evaluates ticket priority, determines the best routing department, and conducts sentiment analysis. An integrated evaluation framework measures model performance using key metrics (precision, recall, F1, accuracy).

📦 Module: ticket_analyzer.models.ticket
Classes
Ticket
A data model representing an incoming support ticket.

Attributes:

ticket_id (str): Unique ticket identifier.

customer_tier (str): Customer tier, e.g., 'free', 'premium', 'enterprise'.

subject (str): Short summary of the issue.

message (str): Full description provided by the customer.

previous_tickets (int): Number of past tickets from this customer.

monthly_revenue (float): Monthly revenue from this customer.

account_age_days (int): Days since the account was created.

PriorityAssessment
Represents the LLM-assigned priority of a ticket.

Attributes:

level (str): One of "low", "medium", "high", "critical".

rationale (str): Explanation for the assigned priority.

RoutingRecommendation
Represents the LLM-determined routing destination for a ticket.

Attributes:

department (str): Assigned department.

expected_response_time (str): SLA-compliant response time.

TicketAnalysis
Stores full analysis output of a ticket.

Attributes:

ticket_id (str): Ticket identifier.

priority (Dict): Serialized PriorityAssessment.

routing (Dict): Serialized RoutingRecommendation.

combined_notes (Optional[str]): Additional analyst notes.

⚙️ Module: ticket_analyzer.priority.PriorityAssessor
Class: PriorityAssessor
Assesses the urgency of a support ticket using both LLM-based and rule-based fallbacks.

Key Features:

Utilizes a Meta-LLaMA LLM hosted via Groq API.

Custom prompt engineering for structured JSON output.

Fallback logic for reliability in case of model failure.

Methods:

assess(ticket: Ticket) -> PriorityAssessment: Evaluates the ticket and returns a structured priority.

_fallback_assessment(ticket: Ticket): Rule-based fallback prioritization logic.

cleanup(): Releases LLM resources manually if needed.

llm: Lazily initializes or accesses the LLM client.

🚦 Module: ticket_analyzer.routing.RoutingSpecialist
Class: RoutingSpecialist
Handles routing logic to determine which internal department should handle the ticket, based on ticket content, sentiment, and priority.

Methods:

route(ticket_data: dict, priority: str, sentiment: dict) -> RoutingRecommendation: Determines the department and response time.

cleanup(): Releases underlying LLM resources.

Departments Considered:

security

technical

billing

feature_request

customer_success

😠 Module: ticket_analyzer.sentiment.SentimentAnalyzer
Class: SentimentAnalyzer
Applies a BERT-based sentiment model to classify customer emotions.

Model Used:

distilbert-base-uncased-finetuned-sst-2-english

Methods:

analyze(text: str) -> SentimentResult: Returns a sentiment label and confidence score.

Class: SentimentResult
Attributes:

label ("POSITIVE" | "NEGATIVE" | "NEUTRAL"): Sentiment class.

score (float): Confidence score from the classifier.

📊 Module: ticket_analyzer.evaluator.Evaluator
Class: Evaluator
Evaluates the performance of the Ticket Analyzer system across multiple tickets.

Metrics Tracked:

Routing: precision, recall, F1, accuracy.

Priority: precision, recall, F1, accuracy.

Response Time Appropriateness.

Methods:

evaluate(results: List[TicketAnalysis], expected: List[dict]) -> Dict[str, float]: Compares system output with ground truth.

_evaluate_category(...): Updates metrics per category.

_calculate_metrics(): Returns a dictionary with evaluation results.

_get_expected_time(...): Determines SLA response time based on ticket priority and department.

🧪 Dataset: test_tickets
A synthetic dataset used to test and evaluate the system.

Each Ticket Includes:

ticket_id, subject, message, customer_tier

expected_priority (ground truth)

expected_department (ground truth)

⚙️ Module: ticket_analyzer.models.base
Class: BaseModelConfig
Extends Pydantic BaseModel with support for custom types, and avoids deep copy of non-serializable objects.

📝 Notes
LLM Output Handling: LLM responses are parsed from JSON. Fallback logic ensures graceful degradation.

Security: Ensure API keys (like GROQ_API_KEY) are securely managed using environment variables.

Extensibility: Each component is modular and testable for future integrations like Zendesk, ServiceNow, etc.
