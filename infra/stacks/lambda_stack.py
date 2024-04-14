from aws_cdk import Stack
from constructs import Construct
from lambda_forge import release

from functions.crawl.start_crawl.config import StartCrawlConfig
from infra.services import Services


@release
class LambdaStack(Stack):
    def __init__(self, scope: Construct, context, **kwargs) -> None:

        super().__init__(scope, f"{context.name}-Lambda-Stack", **kwargs)

        self.services = Services(self, context)

        # Crawl
        StartCrawlConfig(self.services)
