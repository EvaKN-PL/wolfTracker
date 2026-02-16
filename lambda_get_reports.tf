resource "aws_lambda_function" "get_reports" {
  filename      = data.archive_file.main.output_path
  function_name = "${var.env}-lambda-get"
  role          = aws_iam_role.main.arn
  handler       = "get_reports.handler"
  code_sha256   = data.archive_file.main.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      LOG_LEVEL   = "info"
      TABLE_NAME  = aws_dynamodb_table.tracker_db.name
    }
  }

  tags = {
    Environment = var.env
    Application = "wolfTracker"
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group_get" {
  name              = "/aws/lambda/${aws_lambda_function.get_reports.function_name}"
  retention_in_days = 14
}

resource "aws_lambda_permission" "api_gw_get" {
  statement_id  = "AllowExecutionFromAPIGatewayGet"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_reports.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"

}