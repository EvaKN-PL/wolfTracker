terraform {
  backend "s3" {
    bucket         = "wolftracker2026" 
    key            = "wolf-tracker/terraform.tfstate"         
    region         = "eu-central-1"
    encrypt        = true                                     
    
  }
}

provider "aws" {
  region = var.region
}