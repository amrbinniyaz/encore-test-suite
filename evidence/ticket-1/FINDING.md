# Ticket 1 — FIRST20 accepted after a completed booking

Status: app defect observed manually; same-session booking history captured. All 30 cases are now synced to Test Management in project Encore Hackathon, folder Encore - Ticket 1. T030 was assigned saved ID TC-309. The post-sync CSV is exported and verified (30 distinct saved IDs, 98 step rows). Exact clean replay is complete through Test Companion and reproduced the defect; see [clean replay](clean-replay.md).

## Submission finding

After a full-price booking without a discount, FIRST20 is incorrectly accepted on the next booking in the same guest session, reducing a $32 Standard seat to $25.60 instead of rejecting the code.

Suggested severity: **Major**. Suggested call: **Fix it**. The eligibility rule produces an incorrect completed booking price, while the booking flow remains usable. These are evidence-based recommendations, not a published organizer answer key. No actual money was charged: payment is mocked by design.

## Coverage gap

Original T012 uses FIRST20 on booking 1 before checking rejection on booking 2. It misses a first completed booking without that code. T013 tests WELCOME15 after a no-discount booking, not FIRST20. The proposed T030 in [coverage review](../ticket-1-coverage-review.md) fills this gap. Its addition to the generated-test panel is verified (30 cases total).

## Expected behavior

[PRD footnote 2](../../PRD.md) limits FIRST20 to the first completed booking of a session, whether or not it was used on that booking. After any completed booking, FIRST20 must be rejected and a $50 selection must remain $50.

## Observed sequence

1. User screenshot: Discount Code screen showed an empty code field, no applied-code label, and $36 subtotal.
2. User screenshot: BK-YAULBU completed for The Understudy, Ashcroft Playhouse, Standard B3, $36.
3. User screenshot: next booking had a $50 subtotal; FIRST20 was then accepted.
4. Agent capture: BK-ZA1ZCM completed for The Winter's Tale, Ashcroft Playhouse, Standard B1, with FIRST20 and Total Paid $40.
5. Agent capture: My Bookings showed BK-ZA1ZCM ($40) and BK-YAULBU ($36) together in the same running session, corroborating continuity.

The browser header identified Google Pixel 8, Android 14.0. BrowserStack captures were saved September 25, 2026, just after midnight Europe/London; the device screenshot clock showed September 24 around 23:00.

## Saved evidence

- [Discounted confirmation, keyboard visible](05-discounted-booking-confirmation.png)
- [Full confirmation: FIRST20 and Total Paid $40](06-full-discounted-confirmation.png)
- [Same-session history: both confirmation IDs](07-same-session-booking-history.png)

The earlier user screenshots are visible in the conversation but their temporary attachment paths could not be copied. No saved originals for steps 1–3 are claimed. Earlier interaction included applying/removing FIRST20 before the first recorded confirmation; the later [clean replay](clean-replay.md) separately establishes the narrower condition that FIRST20 was never entered or applied before booking 1. The demonstrated violation after a completed booking does not depend on that narrower condition. Do not infer an implementation root cause from this evidence. The later fresh-session execution was performed by Test Companion; no standalone automation script or App Automate public run is claimed.

## Remaining completion steps

- DONE: manually added T030 to the Discount Code scenario and retained the original 29-case backup.
- DONE: exported [30-case local backup](ticket-1-30-cases-unsynced.csv) from Test Companion; CSV has 30 distinct case IDs, including T030 (98 step rows). This is not a post-sync Test Management export.
- DONE: clean TC-309 replay through Test Companion. Booking 1: Late Night Jazz A1, $32 without code, BK-VUUXSA. Booking 2: A2, base $32, FIRST20 accepted, total $25.60, BK-8FXIT4. Both appeared in the same session history. Result: FAIL.
- DONE: synced all 30 cases and exported [final synced CSV](ticket-1-final-synced.csv), including TC-309.
- Submit the finding, severity, call, and product-exported CSV in the official team form. Ticket 1 does not require a GitHub repository.

## Access resolution

Enabled the existing available Test Management product seat for the hackathon account. The browser now reaches Projects rather than Unauthorized. On the next turn, the browser was already inside Projects with onboarding no longer blocking. No terms were accepted by the agent. Created Encore Hackathon and Encore - Ticket 1 in the IDE; observed successful addition of 30 cases and verified the saved CSV.
