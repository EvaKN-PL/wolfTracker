resource "aws_lambda_function" "update_reports" {
  filename      = data.archive_file.main.output_path
  function_name = "${var.env}-lambda-update"
  role          = aws_iam_role.main.arn
  handler       = "update_reports.handler"
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

resource "aws_lambda_permission" "update_report_api" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_reports.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.main.execution_arn}/*/*"
}

