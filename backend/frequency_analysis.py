
from collections import Counter
from backend.preprocessing import extract_keywords

def calculate_keyword_frequency(data):
    all_keywords = []

    for query in data["search_query"].dropna():
        keywords = extract_keywords(query)
        all_keywords.extend(keywords)

    frequency = Counter(all_keywords)

    result = [
        {"Keyword": keyword, "Frequency": count}
        for keyword, count in frequency.most_common()
    ]

    return result


def calculate_query_frequency(data):
    queries = (
        data["search_query"]
        .dropna()
        .str.lower()
        .str.strip()
    )

    result = (
        queries.value_counts()
        .rename_axis("Search Query")
        .reset_index(name="Frequency")
    )

    return result
