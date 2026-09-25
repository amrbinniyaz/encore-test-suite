# TC-309 Execution Report — Clean Replay
**Test Case:** TC-309 — FIRST20 rejected after first completed booking without a discount  
**Project:** Encore Hackathon | Folder: Encore - Ticket 1  
**Executed:** 2026-09-25, Europe/London (BrowserStack session 0e60cbd8ba2ab1825402a57119920c43a3d16e84)  
**Device:** Samsung Galaxy S23, Android  
**App:** encore-release.apk (bs://cb5d83b3d4019552592fa27ba9bef69ca7342fa9)  
**Session type:** Fresh guest session — zero prior completed bookings at start

---

## Preconditions Met
- App launched fresh via "Continue as Guest" — no login, no prior bookings
- No discount code entered or applied at any point during Booking 1
- Same session maintained throughout (no restart, no clear between bookings)

---

## Booking 1 — Full Price, No Discount

| Field | Value |
|---|---|
| Event | Late Night Jazz, Blue Note Café, Fri Oct 9 2026 · 9:30 PM |
| Seat | A1 · Standard |
| Full base price | $32.00 |
| Discount code entered | None |
| Subtotal | $32.00 |
| Total paid | $32.00 |
| **Confirmation ID** | **BK-VUUXSA** |

**Observation:** Payment screen showed Seat A1 · Standard $32.00, Subtotal $32.00, Total USD 32.00. No discount row present. Confirmation screen showed "Booking Confirmed", Total Paid $32.00.

---

## Booking 2 — FIRST20 Applied (Same Session, Different Seat)

| Field | Value |
|---|---|
| Event | Late Night Jazz, Blue Note Café, Fri Oct 9 2026 · 9:30 PM |
| Seat | A2 · Standard (different from Booking 1's A1) |
| Full base price P | $32.00 |
| Discount code entered | FIRST20 |
| Expected result | Rejection — code invalid after first completed booking |
| **Actual result** | **Code ACCEPTED — discount applied** |
| Discount amount | -$6.40 |
| Checkout total | USD 25.60 |
| Applied-code message | "Discount applied: FIRST20" (on confirmation screen, resource-id: confirmation-discount-code) |
| **Confirmation ID** | **BK-8FXIT4** |

---

## My Bookings (Same Session — Both IDs Visible)

| Confirmation | Event | Seat | Amount |
|---|---|---|---|
| BK-8FXIT4 | Late Night Jazz | Seat A2 · Standard | $25.60 |
| BK-VUUXSA | Late Night Jazz | Seat A1 · Standard | $32.00 |

Both bookings appeared in My Bookings within the same uninterrupted guest session.

---

## Verdict: **FAIL**

**Expected:** FIRST20 rejected on Booking 2 with an error message; total remains $32.00.  
**Actual:** FIRST20 accepted; discount of -$6.40 applied; mocked booking total $25.60 instead of $32.00. No real payment was made.

The app does not enforce the "first booking only" restriction for FIRST20 within the same guest session. A user who completes one full-price booking can immediately apply FIRST20 to a second booking and receive a 20% discount they are not entitled to.

---

## Evidence Links

- BrowserStack session: `0e60cbd8ba2ab1825402a57119920c43a3d16e84`
- Device: Samsung Galaxy S23, Android
- App: encore-release.apk

---

## Observations vs Assumptions

### Observations (directly read from device UI)
- Booking 1 confirmation number: BK-VUUXSA, Total Paid $32.00, no discount row on payment screen
- Seat A1 shown as "booked" on seat map when returning for Booking 2 (confirms session continuity)
- FIRST20 entered in `discount-input` field; Apply button clicked
- `discount-applied-label` ViewGroup appeared after Apply; "Remove" button (resource-id: `discount-remove-button`) became visible
- Payment screen for Booking 2: `payment-discount-row` showed "Discount (FIRST20)" with value "-$6.40"; `payment-total` showed "USD 25.60"
- Confirmation screen: `confirmation-discount-code` TextView showed "Discount applied: FIRST20"; `confirmation-price` showed "$25.60"
- My Bookings: both BK-8FXIT4 ($25.60) and BK-VUUXSA ($32.00) visible in same session

### Requirement source and evidence limits
- FIRST20 eligibility comes from PRD footnote 2 in `encore-test-suite/PRD.md`: valid only on the first completed booking of a session, whether or not it was used on that booking. This is an explicit requirement, not an assumption.
- The discount label TextView text was empty/truncated in the page source at the discount screen step; the presence of `discount-applied-label` and the "Remove" button is treated as evidence of acceptance (confirmed by the payment screen discount row)
- "20% off" is the discount rate (32.00 × 0.20 = 6.40 ✓ — arithmetic confirms 20% was applied)

## Review notes

This report was produced by Test Companion during the observed UI workflow and reviewed by Codex. The original generated report incorrectly labelled the execution year as 2025; it has been corrected to the local execution date. Exact Android version and a shareable session URL were not supplied. The session ID above is recorded as reported, not presented as a verified public link. No separate clean-replay PNG files were exported; prior manual-run screenshots remain in this evidence folder.
