# Ticket 1 — review of the original 29 cases

Reviewed source: ticket-1-original-cases.md, cases T001–T029.
Expected behavior source: ../PRD.md, discount footnote 2.
Status: coverage review complete. Related manual execution demonstrated FIRST20 accepted after a completed booking; see ticket-1/FINDING.md. T030 has been manually added and all 30 cases synced to Test Management; saved missing case ID is TC-309. Final CSV: ticket-1/ticket-1-final-synced.csv. Exact fresh-session replay completed through Test Companion and failed the FIRST20 eligibility expectation; see ticket-1/clean-replay.md.

## Definite uncovered condition

FIRST20 must become invalid after the first completed booking in the session, even when it was never used on that booking.

T012 uses FIRST20 on booking 1, then checks rejection on booking 2. An incorrect implementation that merely limits code redemption to one use would pass T012. T013 completes booking 1 without a discount, but subsequently tests WELCOME15 rather than FIRST20. None of the other original cases exercises FIRST20 after an undiscounted first completed booking.

This is a demonstrated coverage gap, not proof that Encore implements the rule incorrectly.

## T030 — FIRST20 rejected after first completed booking without a discount

Preconditions:
- A documented fresh Encore guest session with no completed bookings.
- Available Standard seats; verify the selected seats' actual tiers and prices.
- Preserve the same session throughout the two bookings. Do not restart, reinstall, or clear app data between them.

Steps and expected results:
1. Complete booking 1 with one available Standard seat and no discount. Expected: confirmation appears, full price paid, booking listed in My Bookings.
2. Within the same session, start booking 2 using a different available Standard seat. Record its full price P. Expected: correct seat and base price appear.
3. Enter FIRST20 and tap Apply. Expected: code rejected as ineligible, with an inline error and no applied discount.
4. Continue to Payment without a valid discount. Expected: checkout remains available, discount is zero, total equals P rather than 0.8*P.
5. Complete the mocked payment. Expected: confirmation and My Bookings record booking 2 at P.

Evidence to record:
- First booking confirmation showing no discount.
- Second booking code application result and payment total.
- Device/OS, date, seat IDs, event, base prices, and confirmation numbers.
- Screenshot(s) or recording of the decisive steps.
- Observed behavior, severity and call only after execution.

Suggested Test Companion request:

> Add T030 exactly as described in evidence/ticket-1-coverage-review.md without modifying the original 29 cases. Execute T030 on Encore with a fresh guest session, keeping both bookings in the same session. Record actual results and evidence for each step; do not infer a failure from the coverage gap. Report whether FIRST20 is rejected on the second booking despite never being used on the first. Preserve the result locally if Test Management remains unauthorized.

## Additional issues in the generated set

- T004 and T028 mention all five categories but omit Comedy from explicit expected-result lists. Review actual assertions rather than titles.
- No explicit case checks abandonment before payment or inventory independence between distinct events sharing a venue. Do not describe T030 as the only possible gap in this generated set.
- T016 describes discount as negative, then says Total = Subtotal - Discount. With a signed negative discount the arithmetic should be addition, or subtraction using the discount magnitude.
- T023 requires SAVE10 acceptance for a VIP-only booking, while the PRD only requires no VIP discount; code acceptance is not explicitly specified there.
- The T014 note reports absence of an error from accessibility/page source. That alone does not prove no visible error existed. Verify the screen before claiming an app defect.
- Several cases prescribe exact UI wording or formatting not mandated by the PRD. Separate observed UI details from product requirements.

## Submission remaining

Completed: manual case addition, clean execution, finding assessment, syncing all 30 cases, and final CSV export. Saved missing-case ID: TC-309. Remaining: include the one-sentence finding, recommended Major severity / Fix it call, and ticket-1/ticket-1-final-synced.csv in the official team submission. The original backup remains unchanged.
