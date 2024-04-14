from aws_cdk import aws_lambda as _lambda


class Layers:
    def __init__(self, scope) -> None:

        self.requests_layer = _lambda.LayerVersion.from_layer_version_arn(
            scope,
            id="RequestsLayer",
            layer_version_arn="arn:aws:lambda:eu-west-2:770693421928:layer:Klayers-p39-requests:19",
        )

        self.bs4_layer = _lambda.LayerVersion.from_layer_version_arn(
            scope,
            id="BS4Layer",
            layer_version_arn="arn:aws:lambda:eu-west-2:770693421928:layer:Klayers-p39-beautifulsoup4:7",
        )
