"""
VeriSight Semantic Similarity Engine
Ranks trusted news articles by similarity to a user's claim.
"""

from sentence_transformers import SentenceTransformer, util

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_articles(claim, articles, top_k=5):
    """
    Compare a claim against trusted news articles.

    Args:
        claim (str)
        articles (list)
        top_k (int)

    Returns:
        list of ranked articles
    """

    if not articles:
        return []

    corpus = []

    for article in articles:

        text = f"{article['title']} {article['summary']}"

        corpus.append(text)

    claim_embedding = model.encode(
        claim,
        convert_to_tensor=True
    )

    corpus_embeddings = model.encode(
        corpus,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        claim_embedding,
        corpus_embeddings
    )[0]

    ranked = []

    for article, score in zip(articles, similarities):

        ranked.append(
            {
                "source": article["source"],
                "title": article["title"],
                "summary": article["summary"],
                "link": article["link"],
                "similarity": float(score)
            }
        )

    ranked.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return ranked[:top_k]


if __name__ == "__main__":

    sample_claim = "NASA discovers water on Mars"

    sample_articles = [
        {
            "source": "Reuters",
            "title": "NASA confirms water on Mars",
            "summary": "Scientists announce new evidence.",
            "link": ""
        },
        {
            "source": "BBC",
            "title": "Premier League transfers",
            "summary": "Football transfer news.",
            "link": ""
        }
    ]

    results = rank_articles(
        sample_claim,
        sample_articles
    )

    for article in results:

        print(
            article["similarity"],
            article["title"]
        )