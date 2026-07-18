import math
import re
from collections import Counter

from .documents import Section


def tokens(text: str) -> list[str]:
    return re.findall(r"[^\W_]+", text.casefold().replace("ё", "е"))


def search(sections: list[Section], question: str, limit: int = 3) -> list[Section]:
    terms = set(tokens(question))
    counts = [Counter(tokens(f"{s.title} {s.title} {s.text}")) for s in sections]
    weights = {}
    for term in terms:
        matches = sum(term in count for count in counts)
        weights[term] = math.log((1 + len(sections)) / (1 + matches)) + 1

    ranked = []
    for section, count in zip(sections, counts):
        score = sum(weights[t] * math.log1p(count[t]) for t in terms)
        if score:
            ranked.append((score, section))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [section for _, section in ranked[:limit]]
