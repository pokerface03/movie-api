terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

# Create a security group
resource "aws_security_group" "ec2_sg" {
  name        = "ec2_sg"
  description = "Allow SSH inbound"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an EC2 instance
resource "aws_instance" "tofu_ec2" {
  ami           = "ami-049442a6cf8319180" # Ubuntu server 24.04 
  instance_type = "t3.nano"

  key_name = "awskeyfparmakli"   # Must exist in AWS

  security_groups = [aws_security_group.ec2_sg.name]

  tags = {
    Name = "MyOpenTofuEC2"
  }
}

output "public_ip" {
  value = aws_instance.tofu_ec2.public_ip
}
