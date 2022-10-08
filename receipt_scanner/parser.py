import re


def get_items_from_text(text: str) -> list[str]:
    price_pattern = r"([0-9]+\.[0-9]+)"
    return list(
        map(
            lambda x: x.strip(),
            filter(lambda x: re.search(price_pattern, x) is not None, text.split("\n")),
        )
    )
