resource "aws_lambda_function" "delete_reports" {
  filename      = data.archive_file.main.output_path
  function_name = "${var.env}-lambda-delete"
  role          = aws_iam_role.main.arn
  handler       = "delete_reports.handler"
  code_sha256   = data.archive_file.main.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      LOG_LEVEL  = "info"
      TABLE_NAME = aws_dynamodb_table.tracker_db.name
    }
  }

  tags = {
    Environment = var.env
    Application = "wolfTracker"
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group_del" {
  name              = "/aws/lambda/${aws_lambda_function.delete_reports.function_name}"
  retention_in_days = 14
}

resource "aws_lambda_permission" "api_gw_del" {
  statement_id  = "AllowExecutionFromAPIGatewayDelete"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_reports.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"

}