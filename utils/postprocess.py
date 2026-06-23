import re


# Эти слова никогда не должны попадать в поиск
BANNED_WORDS = {
    "bitrix24",
    "bitrixgpt",
    "яндекс",
    "сбер",
    "ozon",
    "wildberries"
}


# Эти фразы убираем из начала поисковых терминов
PREFIXES = [
    "опыт с ",
    "опыт работы с ",
    "работа с ",
    "знание ",
    "умение ",
    "понимание ",
    "владение ",
    "навык ",
    "навыки "
]


def clean_term(term: str) -> str:
    """Очищает один поисковый термин"""

    term = term.strip()

    for prefix in PREFIXES:
        if term.lower().startswith(prefix):
            term = term[len(prefix):]

    term = term.strip()

    return term


def clean_list(items):
    """Очищает список поисковых терминов"""

    result = []
    used = set()

    for item in items:

        item = clean_term(item)

        if not item:
            continue

        if item.lower() in BANNED_WORDS:
            continue

        if item.lower() in used:
            continue

        used.add(item.lower())

        result.append(item)

    return result


def postprocess(data):

    data["must_have"] = clean_list(data.get("must_have", []))

    data["any_words"] = clean_list(data.get("any_words", []))

    data["exclude"] = clean_list(data.get("exclude", []))

    return data