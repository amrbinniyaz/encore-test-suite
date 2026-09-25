# Encore — teammate handoff

Tickets 1–4 have evidence packages ready for team review. Ticket 5 remains blocked by BrowserStack App Accessibility plan access. No team submission has been sent. Labels below are recommendations for the team to review, not an organizer answer key.

## Review Tickets 1–4

| Ticket | Finding | Recommended severity / call | Evidence |
| --- | --- | --- | --- |
| 1 | FIRST20 is accepted after an earlier completed booking without a discount; $32 becomes $25.60 on booking 2. | Major / Fix it | [Report](evidence/ticket-1/FINDING.md), [final Test Management CSV](evidence/ticket-1/ticket-1-final-synced.csv), [clean replay](evidence/ticket-1/clean-replay.md) |
| 2 | SAVE10 incorrectly discounts VIP as well as Standard seats; mixed-tier total is $166.50 instead of $178.50. | Major / Fix it | [Report, screenshot and public run](evidence/ticket-2/README.md), [automation script](python/tests/test_save10_mixed_tiers.py) |
| 3 | Same event time uses 19:30 on Android 11 and equivalent 7:30 PM on the three other devices; no shifted date/time observed. | Minor / Ship it with a workaround | [Device matrix, four public sessions and screenshots](evidence/ticket-3/README.md) |
| 4 | VIP A1 payment stays processing throughout the 30-second wait. Classification: App Bug. | Critical / Block the release until it's resolved | [Bug report and public session](evidence/ticket-4/README.md), [IDE RCA screenshot](evidence/ticket-4/failure-analysis-rca.png), [app screenshot](evidence/ticket-4/vip-payment-at-60s.png) |

Each linked report contains the reproduction steps, expected/actual behavior, supporting evidence and limitations. BrowserStack public run links for Tickets 2–4 were checked in Incognito when collected. Credentials and private local configuration files are excluded.

### Ticket 1: use the correct CSV

Download **ticket-1-final-synced.csv** for the form: it is the post-sync Test Management export, with 30 distinct saved case IDs including added case TC-309. The other CSV is an earlier unsynced backup and is not the final submission artifact. The coverage review explains the missed condition in the original 29 cases.

Ticket 1 screenshots document the earlier manual run. The clean-replay report separately records the fresh-session $32/$25.60 reproduction; no separate clean-replay screenshot or verified public session URL is claimed.

### Ticket 3: interpretation matters

Four passing tests only prove nonempty date text. The screenshots and actual date strings show the formatting difference. The suggested workaround is explaining equivalent 12/24-hour times; no device-settings workaround was tested. Exact OS versus locale/hour-cycle cause is unconfirmed.

### Ticket 4: avoid an unsupported root cause

The original test was left unchanged. Its spinner wait failed; the later confirmation wait never executed. Failure Analysis returned PRODUCT_BUG, but its initial libpenguin.so causal explanation was not established by evidence. The RCA review preserves that distinction. One device/seat was observed; do not claim every VIP booking or all users were tested.

## Teammate action: Ticket 5

Please check App Accessibility access using your own hackathon BrowserStack/Test Companion login. Our Basic and Advanced + AI session attempts were refused with **You cannot run automation builds on the current plan**, and the dashboard displayed **Your plan has expired**.

If your account has access:

1. In Test Companion App mode, select the official Encore APK.
2. Ask it to navigate as Guest to Neon Skyline seat selection and run a real accessibility scan (WCAG 2.2 AA was our chosen target).
3. Review the most severe actual finding. Record exact rule/WCAG criterion, affected element, scanner severity, recommended fix and practical user impact.
4. Send the exported scan CSV or public report URL, plus a screenshot of the flagged element. Verify a public URL in Incognito.
5. Recommend the ticket Severity and Call separately from the scanner label. Record your name as the actual contributor.

If access is denied, ask the organizer to restore App Accessibility access. Do not mark Ticket 5 complete using an invented scan or manual inspection presented as scanner output.

## Before team submission

- Finish required Ticket 5 and ensure each member genuinely completed at least one ticket.
- Agree the team name, both members' names/emails, contribution ownership, final labels and evidence links.
- Confirm with the organizer that the event's two-person team arrangement overrides the webpage's 4–5-member format.
- Submit one team form before the organizer's deadline. Optional tickets 6–9 can add scoring opportunities if time remains.
- [Official brief and submission link](https://aixtesting-bootcamp.vercel.app/events/team/#submit).

Sharing this GitHub page with a teammate does not submit the official form.
