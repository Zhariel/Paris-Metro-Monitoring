terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.5.0"
    }
  }
}

resource "aws_db_instance" "default" {
  identifier             = var.identifier_RDS
  allocated_storage      = 20
  engine                 = "mysql"
  engine_version         = "8.0.28"
  instance_class         = "db.t3.micro"
  name                   = var.name_RDS
  username               = var.username_RDS
  password               = var.psw_RDS
  vpc_security_group_ids = ["${aws_security_group.instance_sg.id}"]
  publicly_accessible    = true
}

resource "aws_key_pair" "admin2" {
  key_name   = var.key_name
  public_key = var.public_key_value
}

resource "aws_security_group" "instance_sg" {
  name = "terraform-sg"
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "TCP"
    cidr_blocks = ["0.0.0.0/0"]
  }
    ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "TCP"
    cidr_blocks = ["::/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "TCP"
    cidr_blocks = ["::/0"]
  }
}

provider "aws" {
  region = var.aws_region
}



resource "aws_instance" "server" {
  ami                    = var.ami_value
  instance_type          = "t2.micro"
  key_name               = var.key_EC2
  vpc_security_group_ids = ["${aws_security_group.instance_sg.id}"]
  connection {
    type        = "ssh"
    user        = "ec2-user"
    host        = self.public_ip
    private_key = file("C:/local/PA/terraform/ssh-key/id_rsa_aws")
  }
  provisioner "remote-exec" {
    inline = [
      "sudo yum -y install git",
      "sudo yum -y install node",
      "git clone https://github.com/Zhariel/Paris-Metro-Monitoring.git",
      "cd Paris-Metro-Monitoring/app/frontend",
      "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash",
      ". ~/.nvm/nvm.sh",
      "nvm install --lts",
      "npm install",
      "npm start"
    ]
  }
}