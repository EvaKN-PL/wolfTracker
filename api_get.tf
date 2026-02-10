resource "aws_apigatewayv2_integration" "get_reports" {
    api_id = aws_apigatewayv2_api.main.id
    integration_type = "AWS_PROXY"
    integration_uri = aws_lambda_function.get_reports.invoke_arn
  
}

resource "aws_apigatewayv2_route" "get_reports" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "GET /tracks"

  target = "integrations/${aws_apigatewayv2_integration.get_reports.id}"
}