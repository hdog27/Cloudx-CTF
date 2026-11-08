# Cloudx-CTF phase 1: one small, instructor-only AWS Linux lab.
# This is not yet an automated student-facing CTF platform.
# No inbound network ports are opened. Administration is through AWS SSM.

data "aws_ssm_parameter" "al2023_ami" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

locals {
  tags = {
    Project     = var.lab_name
    ManagedBy   = "Terraform"
    Environment = "prototype"
  }
}

resource "aws_vpc" "lab" {
  cidr_block           = "10.72.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(local.tags, { Name = "${var.lab_name}-vpc" })
}

resource "aws_subnet" "lab" {
  vpc_id                  = aws_vpc.lab.id
  cidr_block              = "10.72.1.0/24"
  map_public_ip_on_launch = false

  tags = merge(local.tags, { Name = "${var.lab_name}-subnet" })
}

# The instance requires outbound HTTPS for AWS Systems Manager.
# A public IP + internet gateway avoids NAT/VPC endpoint hourly charges
# for this cheap proof of concept. The security group has ZERO inbound rules.
resource "aws_internet_gateway" "lab" {
  vpc_id = aws_vpc.lab.id
  tags   = merge(local.tags, { Name = "${var.lab_name}-igw" })
}

resource "aws_route_table" "lab" {
  vpc_id = aws_vpc.lab.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab.id
  }

  tags = merge(local.tags, { Name = "${var.lab_name}-routes" })
}

resource "aws_route_table_association" "lab" {
  subnet_id      = aws_subnet.lab.id
  route_table_id = aws_route_table.lab.id
}

resource "aws_security_group" "lab" {
  name_prefix = "${var.lab_name}-"
  description = "Cloudx-CTF instructor POC: no inbound access, HTTPS egress only"
  vpc_id      = aws_vpc.lab.id

  # No ingress block: neither SSH nor lab services are exposed to the internet.
  egress {
    description = "Outbound HTTPS for SSM and required AWS services"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.tags, { Name = "${var.lab_name}-sg" })

  lifecycle {
    create_before_destroy = true
  }
}

data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lab" {
  name_prefix        = "${var.lab_name}-ec2-"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
  tags               = local.tags
}

resource "aws_iam_role_policy_attachment" "ssm" {
  role       = aws_iam_role.lab.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "lab" {
  name_prefix = "${var.lab_name}-"
  role        = aws_iam_role.lab.name
  tags        = local.tags
}

resource "aws_instance" "lab" {
  ami                         = data.aws_ssm_parameter.al2023_ami.value
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.lab.id
  vpc_security_group_ids      = [aws_security_group.lab.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.lab.name
  user_data                   = file("${path.module}/bootstrap.sh")
  user_data_replace_on_change = true

  # T3 standard avoids unexpected unlimited CPU credit charges.
  credit_specification {
    cpu_credits = "standard"
  }

  root_block_device {
    volume_size           = 8
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  tags = merge(local.tags, { Name = "${var.lab_name}-instance" })

  depends_on = [
    aws_iam_role_policy_attachment.ssm,
    aws_route_table_association.lab
  ]
}
