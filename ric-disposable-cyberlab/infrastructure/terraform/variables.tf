variable "aws_region" {
  description = "AWS Region for the first lab prototype."
  type        = string
  default     = "us-east-1"
}

variable "lab_name" {
  description = "Tag and resource name prefix (keep short and lowercase)."
  type        = string
  default     = "cloudx-poc"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,19}$", var.lab_name))
    error_message = "lab_name must be 3-20 lowercase letters, digits or hyphens and start with a letter."
  }
}

variable "instance_type" {
  description = "EC2 size for the disposable Linux proof of concept."
  type        = string
  default     = "t3.micro"

  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Use an x86_64 T3 size supported by the selected AMI."
  }
}
