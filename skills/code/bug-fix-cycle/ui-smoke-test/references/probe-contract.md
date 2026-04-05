# Probe Contract

`verification_loop.py` expects the probe command to print one JSON object to stdout.

## Required Field

- `status`

Allowed values:

- `pass`
- `sample_mismatch`
- `auth_expired`
- `env_blocked`
- `fail`

## Recommended Fields

- `claim_no`
- `claim_id`
- `item_id`
- `item2_id`
- `response_status`
- `evidence`
- `snippet`

## Example Output

```json
{
  "status": "pass",
  "claim_no": "11000026040200200019",
  "claim_id": 202632255819,
  "response_status": 200,
  "evidence": "费用承担部门与报账平台配置的对应费用承担部门不一致，请联系业务财务确认！"
}
```

## Example API Probe

```bash
node scripts/sit_api_probe.mjs \
  --state /Users/xiaoqi/Documents/work/yili/.auth/coding-state.json \
  --base-url https://pri-fssc-web-sit.digitalyili.com \
  --flow resolve-load-submit \
  --claim-no 11000026040200200019 \
  --load-endpoint /api/claim/eer/T002/load \
  --submit-endpoint /api/claim/eer/T002/submit \
  --classify-js "lastText.includes('报账单已删除，不能提交！') ? 'pass' : 'sample_mismatch'"
```

## Example Loop

```bash
python3 scripts/verification_loop.py \
  --bug-id 5200 \
  --candidates-json /tmp/5200-candidates.json \
  --probe-command "node scripts/sit_api_probe.mjs \
    --state /Users/xiaoqi/Documents/work/yili/.auth/coding-state.json \
    --base-url https://pri-fssc-web-sit.digitalyili.com \
    --flow resolve-load-submit \
    --claim-no {claim_no} \
    --load-endpoint /api/claim/eer/T002/load \
    --submit-endpoint /api/claim/eer/T002/submit \
    --classify-js \"lastText.includes('报账单已删除，不能提交！') ? 'pass' : 'sample_mismatch'\""
```

## Example Page Probe

```bash
node scripts/fast_page_probe.mjs \
  --state /Users/xiaoqi/Documents/work/yili/.auth/coding-state.json \
  --base-url https://pri-fssc-web-sit.digitalyili.com \
  --url "/#/claim/otc/T045?claimId=202632231756" \
  --wait-text "单位（件）"
```
