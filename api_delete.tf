resource "aws_apigatewayv2_integration" "delete_reports" {
    api_id = aws_apigatewayv2_api.main.id
    integration_type = "AWS_PROXY"
    integration_uri = aws_lambda_function.delete_reports.invoke_arn

    payload_format_version = "2.0"
  
}

resource "aws_apigatewayv2_route" "delete_reports" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "DELETE /tracks"

  target = "integrations/${aws_apigatewayv2_integration.delete_reports.id}"
}