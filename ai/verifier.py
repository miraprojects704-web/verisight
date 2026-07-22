"""
VeriSight Verification Engine

Combines:
- RSS news retrieval
- Semantic similarity
- Confidence scoring
- Verdict generation
"""

from .news_search import aggregate_news
from .semantic import rank_articles


class VeriSightVerifier:

    def __init__(self, max_sources=5):
        self.max_sources = max_sources

    def _calculate_confidence(self, similarity):
        """
        Convert cosine similarity (0-1) into a confidence score.
        """

        similarity = max(0.0, min(1.0, similarity))

        confidence = int(similarity * 100)

        return max(50, confidence)

    def _generate_verdict(self, confidence):

        if confidence >= 90:
            return "Likely True"

        elif confidence >= 75:
            return "Mostly Supported"

        elif confidence >= 60:
            return "Mixed Evidence"

        else:
            return "Unverified"

    def verify(self, claim):

        articles = aggregate_news(limit_per_source=3)

        if not articles:

            return (
                "Unavailable",
                0,
                "No trusted news sources could be reached.",
                []
            )

        ranked = rank_articles(
            claim,
            articles,
            top_k=self.max_sources
        )

        if not ranked:

            return (
                "Unavailable",
                0,
                "Unable to compare the claim.",
                []
            )

        top_similarity = ranked[0]["similarity"]

        confidence = self._calculate_confidence(
            top_similarity
        )

        verdict = self._generate_verdict(
            confidence
        )

        reasoning = (
            f"The claim was compared against "
            f"{len(articles)} recent articles from trusted "
            "news organizations using semantic similarity."
        )

        return (
            verdict,
            confidence,
            reasoning,
            ranked
        )


if __name__ == "__main__":

    engine = VeriSightVerifier()

    verdict, confidence, reasoning, evidence = engine.verify(
        "NASA confirms water on Mars"
    )

    print()

    print("Verdict:", verdict)

    print("Confidence:", confidence)

    print()

    print(reasoning)

    print()

    for item in evidence:

        print(item["source"])

        print(item["title"])

        print(round(item["similarity"], 3))

        print(item["link"])

        print("-" * 60)

    