test_tickets = [
    {
        "ticket_id": "SUP-001",
        "customer_tier": "free",
        "subject": "This product is completely broken!!!",
        "message": "Nothing works! I can't even log in. This is the worst software I've ever used.",
        "previous_tickets": 0,
        "monthly_revenue": 0,
        "account_age_days": 2,
        "expected_priority": "medium",
        "expected_department": "technical"
    },
    {
        "ticket_id": "SUP-002",
        "customer_tier": "enterprise",
        "subject": "Minor UI issue with dashboard",
        "message": "Hi team, just noticed the dashboard numbers are slightly misaligned on mobile view.",
        "previous_tickets": 15,
        "monthly_revenue": 25000,
        "account_age_days": 730,
        "expected_priority": "medium",
        "expected_department": "frontend"
    },
    {
        "ticket_id": "SUP-003",
        "customer_tier": "premium",
        "subject": "Feature Request: Bulk export",
        "message": "We need bulk export functionality for our quarterly reports. Currently doing single exports takes hours.",
        "previous_tickets": 5,
        "monthly_revenue": 5000,
        "account_age_days": 400,
        "expected_priority": "low",
        "expected_department": "product"
    },
    {
        "ticket_id": "SUP-004",
        "customer_tier": "premium",
        "subject": "API rate limits unclear",
        "message": "Getting rate limited but documentation says we should have 1000 requests/hour. We're only getting 500.",
        "previous_tickets": 8,
        "monthly_revenue": 3000,
        "account_age_days": 180,
        "expected_priority": "high",
        "expected_department": "technical"
    },
    {
        "ticket_id": "SUP-005",
        "customer_tier": "enterprise",
        "subject": "Urgent: Security vulnerability?",
        "message": "Our security team flagged that your API responses include internal server paths in error messages.",
        "previous_tickets": 20,
        "monthly_revenue": 50000,
        "account_age_days": 900,
        "expected_priority": "critical",
        "expected_department": "security"
    }
]