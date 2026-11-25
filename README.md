# Umbrella Agent Tools

`GET /paid` returns the Base token price in USD, liquidity in USD, 24h volume in USD, and 24h price change %, sourced live from DexScreener.

**Paid endpoint:** `GET https://umbrella-agent-pay.lengrowth.workers.dev/paid?token=0x4200000000000000000000000000000000000006` — responds HTTP 402; pay 0.01 USDC on Base to `0x6bf8ac13aaf4c928b75998cf06ce256e59936400`, then re-request with `&tx=<hash>`.

```bash
curl -i "https://umbrella-agent-pay.lengrowth.workers.dev/paid?token=0x4200000000000000000000000000000000000006"
# -> HTTP 402 + payment details; pay 0.01 USDC on Base to 0x6bf8ac13aaf4c928b75998cf06ce256e59936400
# re-request with &tx=<hash> to receive the JSON
```

**Why:** no account, no API key, no vendor lock-in, and it costs no LLM inference.
