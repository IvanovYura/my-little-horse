from typing import List

import graphene

from service.log_utils import get_test_logs


class TestLog(graphene.ObjectType):
    date = graphene.DateTime()
    level = graphene.String()
    message = graphene.String()


class Query(graphene.ObjectType):
    test_logs = graphene.List(TestLog)

    def resolve_test_logs(self, info) -> List[TestLog]:
        return [TestLog(**item) for item in get_test_logs()]
