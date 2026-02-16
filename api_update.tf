resource "aws_apigatewayv2_integration" "update_reports" {
    api_id = aws_apigatewayv2_api.main.id
    integration_type = "AWS_PROXY"
    integration_uri = aws_lambda_function.update_reports.invoke_arn

    payload_format_version = "2.0"
  
}

resource "aws_apigatewayv2_route" "update_reports" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "PATCH /tracks"

  target = "integrations/${aws_apigatewayv2_integration.update_reports.id}"
}