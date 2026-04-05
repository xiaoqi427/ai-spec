# DB Fallback

Use DB fallback only after direct samples from Coding or local bug materials are missing or produce `sample_mismatch`.

## Config

This skill expects the same YAML schema as:

`/Users/xiaoqi/Documents/work/yili/ai-spec/skills/code/bug-fix-cycle/db-query/config/db-connection.yaml`

Key fields:

- `host`
- `port`
- `sid`
- `username`
- `password`
- `tool`

## Query Strategy

1. Query both `T_RMBS_CLAIM` and `T_RMBS_CLAIM_HIS`.
2. Filter by exact template `ITEM_ID`.
3. Prefer exact `ITEM2_ID` when the bug provides it.
4. If exact `ITEM2_ID` is absent, fall back to same prefix.
5. Order by `CUR_RECEIVE_DATE DESC`.

## Minimal Output Fields

- `claim_id`
- `claim_no`
- `item_id`
- `item2_id`
- `item3_id`
- `process_state_eng`
- `status`
- source table flag

## What This Fallback Is For

- Sample hunting for SIT verification
- Reproducing the same branch under a nearby business subtype
- Recovering from stale or invalid bug samples

## What This Fallback Is Not For

- Blindly proving a fix with unrelated samples
- Replacing business understanding of the original bug trigger
- Large-scale brute force over the entire table
