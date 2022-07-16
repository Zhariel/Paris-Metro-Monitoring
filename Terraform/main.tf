terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.5.0"
    }
  }
}

resource "aws_db_instance" "default" {
  identifier        = var.identifier_RDS
  allocated_storage = 20
  engine            = "mysql"
  engine_version    = "8.0.28"
  instance_class    = "db.t3.micro"
  name              = var.name_RDS
  username          = var.username_RDS
  password          = var.psw_RDS
}

resource "aws_key_pair" "admin2" {
  key_name   = var.key_name
  public_key = var.public_key_value
}

resource "aws_instance" "server" {
  ami           = var.ami_value
  instance_type = "t2.micro"
  key_name      = var.key_EC2
}


provider "aws" {
  region = var.aws_region
}