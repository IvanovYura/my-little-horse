import graphene
from datetime import datetime


class Logs(graphene.ObjectType):
    date_from = graphene.String(required=True)
    date_to = graphene.String(required=True)
    host_ip = graphene.String()
    timestamp = graphene.Date()
    verb = graphene.String()
    path = graphene.String()
    code = graphene.String()
    user_agent = graphene.String()


class Query(graphene.ObjectType):
    logs = graphene.Field(
        Logs,
        date_from=graphene.String(),
        date_to=graphene.String(),
    )

    def resolve_logs(self, info, date_from, date_to) -> Logs:
        extracted = _extract(date_from, date_to)
        return Logs(
            **extracted
        )


# mock response for test porpuses
def _extract(date_from: str, date_to: str) -> dict:
    return {
        'host_ip': '127.0.0.1',
        'timestamp': datetime.now(),
        'verb': 'GET',
        'path': '/',
        'code': 200,
        'user_agent': 'Mozilla/5.0',
    }


schema = graphene.Schema(query=Query)
