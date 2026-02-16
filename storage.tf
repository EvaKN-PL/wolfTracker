resource "aws_s3_bucket" "photo" {
    bucket = "${var.env}-tracks-photos"
  
}

resource "aws_s3_bucket_cors_configuration" "photo_cors" {
  bucket = aws_s3_bucket.photo.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"] 
    allowed_origins = ["*"]           
    expose_headers  = ["ETag"]
  }
}