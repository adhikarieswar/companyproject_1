from langchain_openai import ChatOpenAI
from ticket_analyzer.models.base import BaseModelConfig
from ticket_analyzer.models.ticket import PriorityAssessment
from pydantic import PrivateAttr
import os
from typing import Optional


class PriorityAssessor(BaseModelConfig):
    _llm: Optional[ChatOpenAI] = PrivateAttr(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        try:
            self._llm = ChatOpenAI(
                openai_api_base="https://api.groq.com/openai/v1",
                openai_api_key=os.getenv("GROQ_API_KEY", "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"),
                model_name="meta-llama/llama-4-maverick-17b-128e-instruct",
                temperature=0,
                max_tokens=1000
            )
        except Exception as e:
            print(f"LLM initialization failed: {str(e)}")
            self._llm = None

    @property
    def llm(self):
        """Accessor for the LLM client"""
        if self._llm is None:
            raise ValueError("LLM client not initialized")
        return self._llm

    def assess(self, ticket) -> PriorityAssessment:
        """Assess ticket priority using LLM with fallback logic"""
        try:
            # Structured prompt for better JSON output
            prompt = f"""
            Analyze this support ticket and determine priority level (critical/high/medium/low).
            Provide output in JSON format with 'level' and 'rationale' keys.

            Ticket Details:
            - Customer Tier: {ticket.customer_tier}
            - Monthly Revenue: ${ticket.monthly_revenue}
            - Subject: {ticket.subject}
            - Message: {ticket.message[:500]}

            Considerations:
            1. Security issues should be critical
            2. Enterprise customers get higher priority
            3. Angry/frustrated tone increases priority
            4. Revenue impact matters
            """

            response = self.llm.invoke(prompt)
            return PriorityAssessment.parse_raw(response.content)

        except Exception as e:
            print(f"Priority assessment failed: {str(e)}")
            return self._fallback_assessment(ticket)

    def _fallback_assessment(self, ticket) -> PriorityAssessment:
        """Fallback logic when LLM fails"""
        # Security issues
        if "security" in ticket.subject.lower() or "vulnerability" in ticket.message.lower():
            return PriorityAssessment(level="critical", rationale="Security issue detected")

        # Angry customers
        angry_keywords = ["broken", "not working", "terrible", "worst", "awful"]
        if any(kw in ticket.message.lower() for kw in angry_keywords):
            return PriorityAssessment(level="high", rationale="Customer frustration detected")

        # Enterprise customers
        if ticket.customer_tier == "enterprise":
            return PriorityAssessment(level="high", rationale="Enterprise customer priority")

        # Feature requests
        if "feature" in ticket.subject.lower() or "request" in ticket.subject.lower():
            return PriorityAssessment(level="low", rationale="Feature request")

        # Default case
        return PriorityAssessment(level="medium", rationale="Standard priority assessment")