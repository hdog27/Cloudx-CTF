# Architecture

## Initial MVP

1. CTFd stores users/teams, challenge descriptions, flags, and scoring.
2. A backend launch function creates a temporary AWS lab.
3. Infrastructure-as-code defines the vulnerable environment.
4. A session record stores launch time and expiration.
5. An expiration event triggers automated cleanup.
6. Student progress remains in CTFd even after the AWS lab is destroyed.

## Design Principle

The disposable AWS environment should not be the system of record for student progress. Scores and solved challenges should persist separately from the temporary lab.
