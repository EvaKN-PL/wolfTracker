resource "aws_s3_bucket" "photo" {
    bucket = "${var.env}-tracks-photos"
  
}