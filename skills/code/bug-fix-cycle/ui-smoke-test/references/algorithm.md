# Candidate Ranking And Retry Algorithm

This skill uses a confidence-first strategy instead of random retry.

## Why

- Test case prioritization research favors front-loading the cases most likely to reveal useful signal early.
- In this workflow, "useful signal" means finding a sample that can actually prove or disprove the fix, not just executing another request.
- Risk-based ordering beats brute-force trial when SIT is slow and login state is fragile.

## Score Model

Each candidate gets a score:

```text
score =
  source_confidence +
  template_fit +
  item2_fit +
  process_state_fit +
  recency_bonus +
  explicitness_bonus
```

### Source Confidence

- `100`: claim number explicitly written in Coding detail with labels like `单号`, `报账单号`, `claimNo`
- `95`: `claimId=...` explicitly written in Coding detail or SIT execution log
- `90`: claim number or claimId written in Coding comments
- `85`: sample written in `sit-execution-log`
- `80`: sample written in `sit-manual-checklist`
- `70`: Oracle fallback, exact same template and exact same `item2Id`
- `55`: Oracle fallback, same template and same `item2Id` prefix
- `40`: Oracle fallback, same template only

### Fit Bonuses

- `+20`: exact same `item2Id`
- `+10`: same `item2Id` prefix
- `+8`: same `processStateEng` hint as the bug
- `+5`: sample appears in more than one source
- `+0..5`: newer `curReceiveDate` ranks earlier

## Retry Policy

Classify every probe result into one of five states:

- `pass`
- `sample_mismatch`
- `auth_expired`
- `env_blocked`
- `fail`

### State Machine

- `pass`
  Stop immediately.
- `sample_mismatch`
  Keep the probe and move to the next candidate.
- `auth_expired`
  Refresh auth state once, then retry the same candidate.
- `env_blocked`
  Retry the same candidate with backoff.
- `fail`
  Stop. This is likely a real regression or a broken assertion.

## Default Backoff

- First retry: `2s`
- Second retry: `5s`
- Third retry: `10s`

Do not keep retrying the environment forever. After the budget is used, return `env_blocked`.

## Practical Rule

One high-confidence candidate is worth more than ten weak ones. The loop should maximize time to first trustworthy verdict, not time to first request.
