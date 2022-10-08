import re


def filter_text(text: str, regular_expression: re.Pattern | None = None) -> list[str]:
    return list(
        map(
            lambda x: x.strip(),
            filter(lambda x: is_a_valid_line(x, regular_expression), text.split("\n")),
        )
    )


def is_a_valid_line(text: str, regular_expression: re.Pattern | None = None) -> bool:
    if regular_expression is None:
        return True
    return regular_expression.search(text) is not None
