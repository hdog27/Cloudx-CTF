# RIC Disposable Cyber Lab

A prototype system for deploying temporary AWS-based cybersecurity lab environments for CTF and training use.

## Problem

Cybersecurity programs and cyber ranges need repeatable hands-on labs, but manually provisioning, resetting, and destroying environments can take time and may leave unused cloud resources running.

## Goal

Allow an instructor or student to launch a temporary isolated AWS lab, complete a CTF challenge, submit a flag, and have the environment automatically destroyed after a defined time limit.

## MVP Scope

- Deploy one temporary AWS lab from infrastructure-as-code
- Support one CTF challenge
- Track lab start time and expiration
- Automatically destroy expired resources
- Submit flags through an existing CTF platform such as CTFd
- Record provisioning time and estimated session cost

## Architecture (initial)

```text
CTFd / Instructor Portal
        |
        v
   Launch Request
        |
        v
API / Lambda Backend
        |
        v
Terraform / CloudFormation
        |
        v
Temporary AWS Lab
        |
        +--> Student completes challenge
        |
        v
Expiration Event
        |
        v
Automatic Teardown
```

## Repository Layout

- `docs/` — business case, customer requirements, architecture, meeting notes
- `infrastructure/` — AWS/Terraform resources
- `backend/` — launch, destroy, and status functions
- `ctf/` — CTFd config and challenge content
- `scripts/` — helper scripts for deployment/testing
- `tests/` — provisioning and teardown validation
- `evidence/` — screenshots, timing/cost evidence, demo notes

## Project Status

Early planning / prototype stage.
