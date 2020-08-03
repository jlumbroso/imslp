
import re
import typing


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "ImslpSearchExpression",
    "ImslpSearchExpressionSubpart",
    "check_search_expr_to_query",
]


ImslpSearchExpressionSubpart = typing.Union[
    str,
    typing.Pattern[str],
    typing.Callable[[str], bool],

]

ImslpSearchExpression = typing.Optional[typing.Union[
    ImslpSearchExpressionSubpart,
    typing.List[ImslpSearchExpressionSubpart],
]]


def check_search_expr_to_query(
        query: str,
        search_expr: ImslpSearchExpression = None,
        case_insensitive: bool = True,
        intersect=True,
):
    if search_expr is None:
        return True

    if isinstance(search_expr, str):
        if case_insensitive:
            query = query.lower()
            search_expr = search_expr.lower()
        return search_expr in query

    elif isinstance(search_expr, typing.Pattern):
        m = search_expr.search(query)
        return m is not None

    elif isinstance(search_expr, typing.Callable):
        return search_expr(query)

    elif isinstance(search_expr, typing.List):

        for search_expr_item in search_expr:
            rec_call = check_search_expr_to_query(
                query=query,
                search_expr=search_expr_item,
                case_insensitive=case_insensitive,
                intersect=intersect,
            )
            if intersect:
                if not rec_call:
                    return False
            else:
                if rec_call:
                    return True

        return intersect

    return False
