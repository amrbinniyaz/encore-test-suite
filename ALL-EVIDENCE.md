# Encore — All Evidence

Evidence for Tickets 1–4 is collected below, including findings, test cases, scripts, screenshots and public test runs. Ticket 5 is pending because BrowserStack App Accessibility access is unavailable. The submission form has not been submitted. Severity and call labels are evidence-based recommendations.

## Tickets 1–4

| Ticket | Finding | Recommended severity / call | Evidence |
| --- | --- | --- | --- |
| 1 | FIRST20 is accepted after an earlier completed booking without a discount; $32 becomes $25.60 on booking 2. | Major / Fix it | [Report](evidence/ticket-1/FINDING.md), [final Test Management CSV](evidence/ticket-1/ticket-1-final-synced.csv), [clean replay](evidence/ticket-1/clean-replay.md) |
| 2 | SAVE10 incorrectly discounts VIP as well as Standard seats; mixed-tier total is $166.50 instead of $178.50. | Major / Fix it | [Report, screenshot and public run](evidence/ticket-2/README.md), [automation script](python/tests/test_save10_mixed_tiers.py) |
| 3 | Same event time uses 19:30 on Android 11 and equivalent 7:30 PM on the three other devices; no shifted date/time observed. | Minor / Ship it with a workaround | [Device matrix, four public sessions and screenshots](evidence/ticket-3/README.md) |
| 4 | VIP A1 payment stays processing throughout the 30-second wait. Classification: App Bug. | Critical / Block the release until it's resolved | [Bug report and public session](evidence/ticket-4/README.md), [IDE RCA screenshot](evidence/ticket-4/failure-analysis-rca.png), [app screenshot](evidence/ticket-4/vip-payment-at-60s.png) |

Each linked report contains the reproduction steps, expected/actual behavior, supporting evidence and limitations. BrowserStack public run links for Tickets 2–4 were checked in Incognito when collected. Credentials and private local configuration files are excluded.

### Ticket 1 — final CSV

Download **ticket-1-final-synced.csv** for the form: it is the post-sync Test Management export, with 30 distinct saved case IDs including added case TC-309. The other CSV is an earlier unsynced backup and is not the final submission artifact. The coverage review explains the missed condition in the original 29 cases.

Ticket 1 screenshots document the earlier manual run. The clean-replay report separately records the fresh-session $32/$25.60 reproduction; no separate clean-replay screenshot or verified public session URL is claimed.

### Ticket 3 — date and time comparison

Four passing tests only prove nonempty date text. The screenshots and actual date strings show the formatting difference. The suggested workaround is explaining equivalent 12/24-hour times; no device-settings workaround was tested. Exact OS versus locale/hour-cycle cause is unconfirmed.

### Ticket 4 — root-cause evidence

The original test was left unchanged. Its spinner wait failed; the later confirmation wait never executed. Failure Analysis returned PRODUCT_BUG, but its initial libpenguin.so causal explanation was not established by evidence. The RCA review preserves that distinction. The observed scope is one device and one VIP seat.

## Ticket 5 — pending accessibility scan

Basic and Advanced + AI session attempts were refused with **You cannot run automation builds on the current plan**. The dashboard displayed **Your plan has expired**. No scan results have been produced.

Required evidence after access is restored:

- Seat-selection accessibility scan and its most severe verified issue.
- Exact WCAG criterion, affected element, recommended fix and user impact.
- Exported scan CSV or public report URL verified in Incognito.
- Screenshot of the flagged element.
- Recommended Severity and Call.

## Submission status

Tickets 1–4 have evidence packages prepared. Required Ticket 5 remains pending. The official submission form has not been submitted.

[Official brief and submission form](https://aixtesting-bootcamp.vercel.app/events/team/#submit)
