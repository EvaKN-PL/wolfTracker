resource "aws_dynamodb_table" "tracker_db" {
  name         = "${var.env}-Tracker"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "report_id"

  attribute {
    name = "report_id"
    type = "S"
  }

  tags = {
    Name        = "Tracker"
    Environment = var.env
  }
}