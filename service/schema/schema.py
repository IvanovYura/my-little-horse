import graphene

from service.schema.access_log_query import Query as AccessLogQuery, Log
from service.schema.test_log_query import Query as TestLogQuery, TestLog


class Query(AccessLogQuery, TestLogQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, types=[Log, TestLog])
