# Ticket 2 — SAVE10 discounts an ineligible VIP seat

**Recommended severity: Major. Call: Fix it.** Checkout remains usable, but the application violates the published discount eligibility rule and undercharges this mixed-tier order by $12.00. These are our triage recommendations, not an organizer-confirmed answer.

## Rule and scenario

[PRD footnote 1](../../PRD.md): SAVE10 gives 10% off Standard-tier seats only; VIP seats must not be discounted.

1. Start a fresh app session and continue as Guest.
2. Open **Neon Skyline** (`evt-01`) at Riverside Arena.
3. Select **VIP A1 ($120.00)** and **Standard C1 ($65.00)**.
4. Apply **SAVE10** and continue to **Review & Pay**.
5. Compare both seat prices, subtotal, discount and final order total against the rule.

| Amount | Expected | Observed |
|---|---:|---:|
| VIP A1 | $120.00 | $108.00 |
| Standard C1 | $58.50 | $58.50 |
| Subtotal before discount | $185.00 | $185.00 |
| Discount | $6.50 | $18.50 |
| Final checkout total | **$178.50** | **$166.50** |

Expected total: `$120.00 + ($65.00 × 0.90) = $178.50`. Actual total is $12.00 too low because the VIP seat also receives 10% off.

## Automation and evidence

- [Saved Appium/pytest script](../../python/tests/test_save10_mixed_tiers.py), generated through BrowserStack Test Companion, then run with the BrowserStack Python SDK.
- [Payment screen from the automated run](payment-screen-save10.png).
- [Raw and parsed prices with calculated expectations](save10-mixed-tiers-evidence.json).
- [BrowserStack public run — final build 2](https://app-automate.browserstack.com/projects/Encore+Hackathon/builds/Encore+Hackathon+Ticket/2?tab=tests&testListView=spec&public_token=6cf685aea634b4e545fb43be189adc6ff942e0be217c6e85ca9a4b927dbc4e20).

The final public build and its three pricing assertion failures were verified in a new Chrome Incognito window without signing in on 25 September 2026 (Europe/London). Both runs used Samsung Galaxy S23, Android 13.0. Final build 2 ran the pushed script at commit `c3d4ff590ccbb656c9addfb65ea93285a4e4df4b`; its BrowserStack source link resolves to that revision. Build duration: 47.28 seconds. The committed screenshot/JSON are from build 2. Pytest reported **1 failed**: the VIP price, discount amount and final total all contradicted the PRD; this was a product assertion failure rather than a navigation/setup failure. Standard pricing and subtotal matched.

The test reads base prices and tiers from the live seat map, calculates expected values with Decimal, and saves JSON and a screenshot before reporting all pricing mismatches. It stops at Review & Pay: it does not finalize this booking. The app's payment is mocked per the PRD. Two automated runs reproduced the same pricing violations. This is evidence of this case, not an exhaustive regression assessment.

## Reproduce

From this fork's `python` directory:

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp browserstack.yml browserstack.local.yml
```

Fill the local, gitignored YAML with your own BrowserStack username/access key, the uploaded frozen `app/encore-release.apk` app ID, Samsung Galaxy S23 and Android 13.0. Use project `Encore Hackathon` and build `Encore Hackathon — Ticket 2`. Keep credentials out of Git.

```sh
BROWSERSTACK_CONFIG_FILE=browserstack.local.yml .venv/bin/browserstack-sdk pytest tests/test_save10_mixed_tiers.py -v
```

The executed script writes fresh evidence to `../evidence/ticket-2` relative to the repository root (a sibling directory). The committed artifacts above are copies from the reported run. A failure with the three price violations is the expected outcome on this frozen buggy build; the assertions should pass after the product is corrected.

## Submission text

> SAVE10 incorrectly discounts VIP seats in a mixed-tier booking. For Neon Skyline, VIP A1 costs $120 and Standard C1 costs $65. SAVE10 should discount only Standard by $6.50, giving a $178.50 final total. The automated run shows VIP $108, Standard $58.50, discount $18.50 and total $166.50: a $12 undercharge. Severity: Major. Call: Fix it. The public BrowserStack run, saved GitHub script and screenshot/JSON substantiate the finding.

This evidence package is ready for the team's consolidated submission; creating it does not submit the team form.
