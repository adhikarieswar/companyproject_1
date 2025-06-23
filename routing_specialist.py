from langchain_openai import ChatOpenAI
from ticket_analyzer.models.ticket import RoutingRecommendation
import os
from contextlib import contextmanager

class RoutingSpecialist:
    def __init__(self):
        self._llm = None  # Initialize as None

    @property
    def llm(self):
        if self._llm is None:
            self._llm= ChatOpenAI(
        openai_api_base="https://api.groq.com/openai/v1",  # Groq API endpoint
        openai_api_key="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",  # Groq API key from environment variable
        model_name="meta-llama/llama-4-maverick-17b-128e-instruct",  # Llama 3 model
        temperature=0,  # Deterministic output
        max_tokens=1000,  # Maximum response length
    )

    def cleanup(self):
        """Explicit cleanup method to call when done"""
        if self._llm and hasattr(self._llm.client, '_client'):
            self._llm.client._client.close()
            self._llm = None

    def route(self, ticket_data: dict, priority: str, sentiment: dict) -> RoutingRecommendation:
        try:
            response = self.llm.invoke(f"""
            Route this {priority} priority ticket:
            Customer: {ticket_data['customer_tier']}
            Sentiment: {sentiment.get('label', 'neutral')}
            Subject: {ticket_data['subject']}

            Departments:
            - security (1hr)
            - technical (4-24hr)
            - billing (24hr)
            - feature_request (1wk)
            - customer_success (8hr)
            """)
            return RoutingRecommendation.parse_raw(response.content)
        except Exception:
            return RoutingRecommendation(
                department="technical",
                rationale="Fallback routing",
                expected_response_time="24 hours"
            )
