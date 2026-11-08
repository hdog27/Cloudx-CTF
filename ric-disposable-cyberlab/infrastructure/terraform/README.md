# Cloudx-CTF — Phase 1 AWS Lab (Draft)

**Status:** Infrastructure-as-code implementation proposed in a review branch. No AWS resources have been deployed or validated yet. This is not a student-ready CTF integration.

## What is implemented in code

- One dedicated VPC, subnet, internet gateway and route table.
- One Amazon Linux 2023 EC2 instance (default `t3.micro`) with encrypted, delete-on-termination EBS storage.
- A security group with **no inbound rules**, and outbound TCP/443 only.
- An instance role using AWS's `AmazonSSMManagedInstanceCore` policy, and IMDSv2 required.
- An example Linux file-permissions challenge initialized at first boot.
- Terraform outputs for instance ID and AWS Systems Manager connection.

**Why a public IP?** The prototype uses a low-cost internet gateway for outbound connections to AWS Systems Manager, without NAT gateways or paid VPC endpoints. The instance has a public IP and public IPv4 charges may apply, but no inbound access is allowed by the security group. The challenge is *not* reachable from the internet. A production student-access design will require separate review.

## Prerequisites

1. An AWS account you control, with permission to create/delete VPC, EC2, IAM, and security group resources, read the public Amazon Linux AMI parameter, and manage an SSM session.
2. AWS CLI installed and configured to the **intended account and region**.
3. Terraform installed locally (project currently uses AWS provider 5.x).
4. A budget/alarm, cost awareness, and a plan to destroy the lab after testing.

No AWS keys or credentials should be stored in this repository.

## Windows PowerShell: first smoke test

From `ric-disposable-cyberlab/infrastructure/terraform`:

```powershell
aws sts get-caller-identity
terraform version
terraform init
terraform fmt -check
terraform validate
terraform plan
```

Review the plan **before** running `terraform apply`, especially the AWS identity, region, estimated number of resources, and expected costs.

When ready to intentionally create billable AWS resources:

```powershell
terraform apply
terraform output -raw lab_instance_id
```

In the AWS console, open **EC2 > Instances > [instance] > Connect > Session Manager** using an IAM identity authorized for SSM. Or, with the Session Manager plugin installed:

```powershell
aws ssm start-session --target (terraform output -raw lab_instance_id) --region (terraform output -raw aws_region)
```

Once inside the instructor's Session Manager shell:

```bash
cat /opt/cloudx-ctf/START-HERE.txt
sudo -iu learner
find /opt/cloudx-ctf -type f
ls -l /opt/cloudx-ctf/legacy-backups/app.conf.bak
cat /opt/cloudx-ctf/legacy-backups/app.conf.bak
exit
sudo chmod 0600 /opt/cloudx-ctf/legacy-backups/app.conf.bak
sudo -iu learner test -r /opt/cloudx-ctf/legacy-backups/app.conf.bak && echo READABLE || echo ACCESS_DENIED
```

## Teardown is REQUIRED after testing

```powershell
terraform destroy
```

Inspect the AWS console afterward to verify that the EC2 instance, its EBS volume, VPC, IAM role, public IP and other prototype resources are removed. Terraform state should be retained securely until cleanup is confirmed. **There is no automatic TTL or timed teardown in this first version.** Destroy is manual.

## Current limitations

- Not deployed or AWS-tested; `terraform plan` / `apply` results are still needed.
- No automated expiration, launch API, per-student access, CTFd API connection or assessment telemetry.
- This single instance has a public IP but no ingress; the exercise is only accessible to an operator through SSM.
- The sample demo flag is in GitHub and **must not be used for real competitive scoring**.
- The Session Manager user may have administrative privileges; it is **not** suitable for untrusted students or exploit-capable labs in this form.
- AWS service costs, quotas and permissions depend on your account, region and use.

## Next small increment

1. Confirm `terraform init`, `validate`, `plan`, `apply`, and `destroy` in the user's AWS account.
2. Add a separately tested, safe time-based cleanup mechanism and independent orphaned-resource checks.
3. Define an authorized student-access workflow and identity boundary.
4. Connect a challenge result or attempt ID to CTFd before broader telemetry work.

See `../../docs/mentor-feedback-roadmap.md` for Wayne Schmidt's longer-term design recommendations.
