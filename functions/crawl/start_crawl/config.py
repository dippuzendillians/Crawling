from infra.services import Services


class StartCrawlConfig:
    def __init__(self, services: Services) -> None:

        crawl_function = services.aws_lambda.create_function(
            name="Crawl",
            path="./functions/crawl",
            description="A function to crawl the website",
            directory="scraper",
            timeout=6,
            layers=[services.layers.requests_layer, services.layers.bs4_layer],
        )

        api_function = services.aws_lambda.create_function(
            name="StartCrawl",
            path="./functions/crawl",
            description="A function to start the crawling",
            directory="start_crawl",
            environment={"TARGET_FUNCTION_ARN": crawl_function.function_arn},
        )

        services.api_gateway.create_endpoint(
            "POST", "/crawl", api_function, public=True
        )

        crawl_function.grant_invoke(api_function)
