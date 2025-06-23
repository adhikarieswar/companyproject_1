from typing import List, Dict, Tuple
from ticket_analyzer.models.ticket import TicketAnalysis


class Evaluator:
    def __init__(self):
        self.metrics = {
            "routing": {
                "true_positives": 0,
                "false_positives": 0,
                "false_negatives": 0,
                "total": 0
            },
            "priority": {
                "true_positives": 0,
                "false_positives": 0,
                "false_negatives": 0,
                "total": 0
            },
            "response_time_appropriate": 0,
            "total_tickets": 0
        }

    def evaluate(self, results: List[TicketAnalysis], expected: List[dict]) -> Dict[str, float]:
        """Evaluate the performance using precision, recall, and F1 metrics."""
        for result, expectation in zip(results, expected):
            self.metrics["total_tickets"] += 1

            # Evaluate routing
            self._evaluate_category(
                "routing",
                result.routing.department,
                expectation["expected_department"]
            )

            # Evaluate priority
            self._evaluate_category(
                "priority",
                result.priority.level,
                expectation["expected_priority"]
            )

            # Check response time
            expected_time = self._get_expected_time(
                result.priority.level,
                result.routing.department
            )
            if result.routing.expected_response_time == expected_time:
                self.metrics["response_time_appropriate"] += 1

        return self._calculate_metrics()

    def _evaluate_category(self, category: str, predicted: str, expected: str):
        """Helper method to update TP, FP, FN counts for a category."""
        self.metrics[category]["total"] += 1

        if predicted == expected:
            self.metrics[category]["true_positives"] += 1
        else:
            self.metrics[category]["false_positives"] += 1
            # For recall, we need to count how many expected positives were missed
            self.metrics[category]["false_negatives"] += 1

    def _calculate_metrics(self) -> Dict[str, float]:
        """Calculate precision, recall, and F1 for all metrics."""
        metrics = {}

        # Routing metrics
        routing_precision = self._calculate_precision("routing")
        routing_recall = self._calculate_recall("routing")
        metrics.update({
            "routing_precision": routing_precision,
            "routing_recall": routing_recall,
            "routing_f1": self._calculate_f1(routing_precision, routing_recall),
            "routing_accuracy": self.metrics["routing"]["true_positives"] / self.metrics["routing"]["total"]
        })

        # Priority metrics
        priority_precision = self._calculate_precision("priority")
        priority_recall = self._calculate_recall("priority")
        metrics.update({
            "priority_precision": priority_precision,
            "priority_recall": priority_recall,
            "priority_f1": self._calculate_f1(priority_precision, priority_recall),
            "priority_accuracy": self.metrics["priority"]["true_positives"] / self.metrics["priority"]["total"]
        })

        # Response time metrics
        metrics["response_time_accuracy"] = (
                self.metrics["response_time_appropriate"] / self.metrics["total_tickets"]
        )

        return metrics

    def _calculate_precision(self, category: str) -> float:
        tp = self.metrics[category]["true_positives"]
        fp = self.metrics[category]["false_positives"]
        denominator = tp + fp
        return tp / denominator if denominator > 0 else 0.0

    def _calculate_recall(self, category: str) -> float:
        tp = self.metrics[category]["true_positives"]
        fn = self.metrics[category]["false_negatives"]
        denominator = tp + fn
        return tp / denominator if denominator > 0 else 0.0

    def _calculate_f1(self, precision: float, recall: float) -> float:
        denominator = precision + recall
        return 2 * (precision * recall) / denominator if denominator > 0 else 0.0

    def _get_expected_time(self, priority: str, department: str) -> str:
        """Determine expected response time based on priority and department."""
        if priority == "critical":
            return "1 hour"
        elif priority == "high":
            return "4 hours"
        elif department == "feature_request":
            return "1 week"
        else:
            return "24 hours"