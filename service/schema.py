from typing import List

import graphene

from service.log_utils import get_logs


class Log(graphene.ObjectType):
    """
    Represents one line in access.log
    """
    host_ip = graphene.String()
    timestamp = graphene.DateTime()
    verb = graphene.String()
    path = graphene.String()
    code = graphene.String()
    user_agent = graphene.String()


class Query(graphene.ObjectType):
    logs = graphene.List(
        Log,
        date_from=graphene.String(required=True),
        date_to=graphene.String(required=True),
    )

    def resolve_logs(self, info, date_from, date_to) -> List[Log]:
        extracted = _extract(date_from, date_to)
        return [Log(**item) for item in extracted]


def _extract(date_from: str, date_to: str) -> List[dict]:
    return get_logs('../resources/access.log', date_from, date_to)


schema = graphene.Schema(query=Query, types=[Log])
