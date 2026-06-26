# utils/postprocess.py

BANNED_WORDS = {
    "bitrix24",
    "bitrixgpt",
    "яндекс",
    "сбер",
    "ozon",
    "wildberries"
}

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
    """Очищает один поисковый термин."""

    term = term.strip()

    for prefix in PREFIXES:
        if term.lower().startswith(prefix):
            term = term[len(prefix):]

    return term.strip()


def clean_list(items):
    """Очищает список терминов, удаляет повторы и запрещённые слова."""

    result = []
    used = set()

    for item in items:

        if not isinstance(item, str):
            continue

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


def build_boolean(must_have):
    """Строит Boolean только из обязательных технологий."""

    if not must_have:
        return ""

    return " AND ".join(f"({term})" for term in must_have)


def postprocess(data):

    must_have = clean_list(data.get("must_have", []))
    any_words = clean_list(data.get("any_words", []))

    # удаляем из any_words всё, что уже есть в must_have
    must_have_lower = {x.lower() for x in must_have}
    any_words = [x for x in any_words if x.lower() not in must_have_lower]

    data["must_have"] = must_have
    data["any_words"] = any_words

    # Boolean всегда строится автоматически
    data["boolean"] = build_boolean(must_have)

    return data