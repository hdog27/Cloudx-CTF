output "aws_region" {
  description = "Region in which the prototype was deployed."
  value       = var.aws_region
}

output "lab_instance_id" {
  description = "Use this ID to locate the instance in the EC2 or Systems Manager console."
  value       = aws_instance.lab.id
}

output "lab_security_group_id" {
  description = "Security group has no inbound rules."
  value       = aws_security_group.lab.id
}

output "lab_vpc_id" {
  description = "Dedicated prototype VPC."
  value       = aws_vpc.lab.id
}

output "operator_session_command" {
  description = "Run after deployment with AWS CLI + Session Manager plugin and appropriate operator IAM permissions."
  value       = "aws ssm start-session --target ${aws_instance.lab.id} --region ${var.aws_region}"
}
