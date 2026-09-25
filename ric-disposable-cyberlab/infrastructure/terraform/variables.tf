variable "aws_region" {
  description = "AWS region for the prototype lab"
  type        = string
  default     = "us-east-1"
}

variable "lab_name" {
  description = "Name prefix for lab resources"
  type        = string
  default     = "ric-disposable-cyberlab"
}
