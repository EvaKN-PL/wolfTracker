# IAM role for Lambda execution
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "main" {
  name               = "${var.env}-lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


data "archive_file" "main" {
  type        = "zip"
  source_file = "${path.module}/index.py"
  output_path = "${path.module}/function.zip"
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.main.function_name}"
  retention_in_days = 14
}

# Policy definition for DynamoDB
resource "aws_iam_policy" "lambda_dynamodb" {
  name        = "${var.env}-lambda-dynamodb-policy"
  description = "Allow write tracks to DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.tracker_db.arn
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.lambda_dynamodb.arn

}

# Lambda function
resource "aws_lambda_function" "main" {
  filename      = data.archive_file.main.output_path
  function_name = "${var.env}-lambda"
  role          = aws_iam_role.main.arn
  handler       = "index.handler"
  code_sha256   = data.archive_file.main.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      ENVIRONMENT = var.env
      LOG_LEVEL   = "info"
      TABLE_NAME  = aws_dynamodb_table.tracker_db.name
    }
  }

  tags = {
    Environment = var.env
    Application = "wolfTracker"
  }
}



