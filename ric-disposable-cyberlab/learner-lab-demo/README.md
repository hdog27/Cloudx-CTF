# Cloudx-CTF — working AWS Academy demo

This is the smallest demonstrable version: **launch a real temporary Linux EC2 lab, fix a file permission, automatically grade the actual machine state, produce a JSON report, and shut the instance down on a timer.**

**This is an instructor-operated proof of concept, not a secure multi-student CTF.** It uses Amazon Linux 2023 and an existing AWS key pair; it intentionally does **not** create IAM roles (which are restricted in some AWS Academy sandboxes).

## One-time prerequisites

- Use your AWS Academy **Learner Lab**, not the separate Cloud Foundations *Sandbox Environment* that deletes resources at the end of each session. Both may be available; check the course's actual instructions.
- Confirm the Learner Lab supports CloudFormation, VPC, EC2, key pairs, and the public AL2023 SSM AMI parameter.
- Open in **us-east-1**. Determine your own public IPv4 address and add **/32**; do not allow SSH from **0.0.0.0/0**.
- You need the private key for an **existing** EC2 key pair in this lab. AWS Academy sometimes supplies one named \`vockey\`. If not, create/select a permitted key pair and update the parameter.
- Check your lab remaining budget. This template provisions one t3.micro EC2 instance, 8 GB gp3 EBS, one public IPv4 address, and basic no-hourly-fee VPC networking. **EC2, EBS, public IPv4, and some transfer may incur charges**; your sandbox allowance and actual AWS pricing determine the total.

## Deploy without installing Terraform

1. In Learner Lab, click **Start Lab** and open the linked **AWS Console** (not Builder ID).
2. Open **CloudFormation → Create stack → With new resources (standard)**.
3. Choose **Upload a template file** and upload [cloudx-demo.yaml](cloudx-demo.yaml).
4. Stack name: \`cloudx-ctf-demo\`. Set **AllowedSshCidr** to your public IP plus \`/32\`; select an existing **key pair**; keep runtime at 90 minutes or lower.
5. Review the resources and create the stack. Do not grant IAM permissions unless you understand why AWS asks.
6. Wait for \`CREATE_COMPLETE\`, then open stack **Outputs** for the instance public IP. The shell bootstrap can take another minute.

If stack creation fails with an authorization error, **stop and record the error**; AWS Academy may restrict a service or resource. Do not bypass school policy.

## Demonstrate the challenge

Connect only from the allowed IP using your downloaded key pair:

\`\`\`powershell
ssh -i "C:\path\to\your-key.pem" ec2-user@PUBLIC_IP_FROM_OUTPUTS
\`\`\`

Inside the instance:

\`\`\`bash
cat /home/learner/README-LAB.txt
sudo cloudx-grade                # baseline: intentionally insecure backup
sudo su - learner
ls -l legacy-backups/app.conf.bak
cat legacy-backups/app.conf.bak
chmod 600 legacy-backups/app.conf.bak
printf '%s\n' 'The backup was readable by other users. I restricted it to the owner and would verify the authorized owner can still read it.' > reflection.txt
exit
sudo cloudx-grade                # expected score 100/100
sudo cat /var/lib/cloudx-ctf/reports/latest-report.json
\`\`\`

To redo the demonstration:

\`\`\`bash
sudo cloudx-reset
sudo cloudx-grade
\`\`\`

The grader checks **real file permissions and actual read access as two different Linux users**. The reflection check only verifies length, **not correctness**. Scores are rule-based; Gemini or other AI is **not integrated in this deployable demo**. Raw commands are not captured or sent to any external API.

## Clean up: absolutely required

The template schedules EC2 termination after the selected runtime. **Automatic instance termination is not full AWS resource cleanup**; VPC, subnet, gateway, routing, and security groups remain until the stack is deleted.

In CloudFormation: select \`cloudx-ctf-demo\` → **Delete**. Verify status and check EC2/EBS networking resources afterward. From the Learner Lab CLI, if permitted:

\`\`\`bash
aws cloudformation delete-stack --stack-name cloudx-ctf-demo --region us-east-1
aws cloudformation wait stack-delete-complete --stack-name cloudx-ctf-demo --region us-east-1
\`\`\`

Never commit \`.pem\` files, credentials, or learner data to GitHub. Do not rely on the classroom sandbox to keep data after the course.

## Cost-analysis evidence for your professor

Record the AWS region, EC2 instance type, runtime, EBS volume size, and the public IPv4 address time. Use AWS pricing or AWS Pricing Calculator to estimate:

\`\`\`text
Estimated attempt cost =
    (EC2 hourly rate × run hours)
  + (8 GB gp3 monthly rate × months used)
  + (public IPv4 hourly rate × allocated hours)
  + transfer/storage charges, if applicable
\`\`\`

Also record screenshots of CloudFormation \`CREATE_COMPLETE\`, the grader's **before/after scores**, and \`DELETE_COMPLETE\`.

## Important limitations

- Initial scope is a **single instructor-controlled host**, not an attackable red-team target; do not give the privileged EC2 login to untrusted students.
- Grading happens inside the lab, not in CTFd. A centralized API and signed reports are future features.
- The Linux exercise is intentionally trivial. There is no separate AI model, cross-cloud orchestration, or student IAM.
- AWS Sandbox/Learner Lab role restrictions may block deployment. No live AWS test has been performed yet.
- Auto termination protects the major compute expense but does not guarantee zero remaining resources.
