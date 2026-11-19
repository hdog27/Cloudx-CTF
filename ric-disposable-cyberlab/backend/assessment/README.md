# Cloudx-CTF — Prototype scoring and optional AI coaching

**Status: tested offline with synthetic data; not connected to AWS or CTFd.**

## Try it (Python standard library only)

Run these commands from this folder:

```powershell
python score_attempt.py sample-attempt.json
python -m unittest -v test_score_attempt.py
```

Sample outcome: **85/100; not passed**, because the remediation did not verify legitimate access was preserved. The core rubric is deterministic. The prototype intentionally requires that both access-control verification checks pass in addition to scoring at least 80.

## Optional Gemini coaching

A Gemini API request is supported, but has **not been live tested**. Obtain your own API key, verify the model ID and current pricing/quotas from [Google's docs](https://ai.google.dev/api/generate-content), then try:

```powershell
$env:GEMINI_API_KEY = 'YOUR_KEY'
python score_attempt.py sample-attempt.json --ai --model YOUR_AVAILABLE_MODEL
Remove-Item Env:GEMINI_API_KEY
```

The backend sends only allowlisted rubric outcomes and score to the model, **not** usernames, raw commands, IP addresses, or captured output. AI provides coaching, never the numeric grade.

## Not implemented yet

- Trusted verifier automatically collecting results from an actual lab.
- CTFd sign-in/integration, learner session association, or instructor reporting UI.
- Telemetry collection, sanitization/storage, consent, access control and retention policies.
- AI provider usage tests, operational quota monitoring, and billing controls.

**Security:** This input JSON is a synthetic example. Do not accept student-controlled `checks` as authoritative results. Trusted independent checks must verify the actual lab state; logged shell commands by themselves do not prove success. Never commit API keys or send raw student telemetry to an external model.

This is a deliberately small first step toward Wayne Schmidt's *Attempt → Observe → Assess → Explain → Adapt → Retry* concept.
