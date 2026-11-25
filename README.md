# Umbrella Agent Tools

Zero-setup on-demand data for autonomous agents. No API key, no signup, no vendor lock-in.

## Token Intel (x402, USDC on Base)

`GET https://umbrella-agent-pay.lengrowth.workers.dev/paid`

Returns a snapshot of a Base token: price, liquidity, 24h volume, 24h change. Cost: **0.01 USDC** on Base. Payment is verified on-chain; the data is released only when the USDC transfer to the payTo address is confirmed.

- **payTo:** `0x6bf8ac13aaf4c928b75998cf06ce256e59936400`
- **Network:** Base mainnet (eip155:8453)
- **Asset:** USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- **Price:** 10000 units (0.01 USDC)

Call without `?tx=` to receive the x402 challenge. Pay, then re-call with `?tx=<txhash>` to receive the data.

Listed on agent-tools.cloud.
