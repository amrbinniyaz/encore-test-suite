# test_save10_mixed_tiers.py
#
# Ticket 2 — SAVE10 mixed-tier discount validation
#
# PRD rule (footnote [^1]): SAVE10 gives 10% off Standard-tier seats ONLY.
# VIP-tier seats must NOT be discounted.
#
# Scenario: book 1 Standard seat (C1) + 1 VIP seat (A1) for "Neon Skyline"
# (evt-01), apply SAVE10, then assert the payment screen shows the
# PRD-correct breakdown.
#
# Base prices are read dynamically from each seat's content-desc on the seat
# map so the test stays correct if prices change.
#
# Expected (computed from live prices S and V):
#   Discount  = 0.10 * S          (Standard only — VIP gets $0 off)
#   Subtotal  = S + V
#   Total     = 0.90 * S + V
#
# Evidence (screenshot + JSON) is saved to evidence/ticket-2/ BEFORE
# assertions so failures are documented even when the test fails.
#
# All pricing mismatches are collected and reported together — the test does
# NOT short-circuit on the first failure.
#
# Run via the BrowserStack Python SDK:
#   cd encore-hackathon-fork/python
#   BROWSERSTACK_CONFIG_FILE=browserstack.local.yml .venv/bin/browserstack-sdk \
#     pytest tests/test_save10_mixed_tiers.py -v
#
# Credentials are read from browserstack.local.yml (gitignored).

import json
import os
import re
from decimal import Decimal, ROUND_HALF_UP

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------------------------------------------------------
# Constants — grounded in live exploration (Samsung Galaxy S23, evt-01)
# ---------------------------------------------------------------------------
EVENT_CARD_ID  = "event-card-evt-01"   # "Neon Skyline" — has VIP rows A/B
VIP_SEAT_ID    = "seat-A1"             # row A = VIP tier
STD_SEAT_ID    = "seat-C1"             # row C = Standard tier
DISCOUNT_CODE  = "SAVE10"

EVIDENCE_DIR   = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "evidence", "ticket-2"
)

NAV_WAIT   = 20   # seconds — screen transitions
INPUT_WAIT = 10   # seconds — element interactions


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def by_id(resource_id):
    """UiAutomator selector by resource-id."""
    return (
        AppiumBy.ANDROID_UIAUTOMATOR,
        f'new UiSelector().resourceId("{resource_id}")',
    )


def wait_for(driver, resource_id, timeout=NAV_WAIT):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(by_id(resource_id))
    )


def parse_price(text: str) -> Decimal:
    """
    Parse a price string robustly.
    Handles: "$120", "USD 166.50", "-$18.50", "-$6.50", "$1,234.56"
    Returns a positive Decimal (sign is stripped — callers handle sign).
    """
    cleaned = re.sub(r"[^\d.,]", "", text)   # keep digits, dot, comma
    cleaned = cleaned.replace(",", "")        # remove thousands separators
    if not cleaned:
        raise ValueError(f"Cannot parse price from {text!r}")
    return Decimal(cleaned).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def is_negative(text: str) -> bool:
    """Return True if the raw text represents a negative/discount amount."""
    return "-" in text


def extract_price_from_content_desc(desc: str) -> Decimal:
    """
    Extract the dollar price from a seat content-desc like:
      "Seat A1, vip, available, $120"
      "Seat C1, standard, selected, $65"
    """
    m = re.search(r"\$(\d+(?:\.\d+)?)", desc)
    if not m:
        raise ValueError(f"No price found in content-desc: {desc!r}")
    return Decimal(m.group(1)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def extract_tier_from_content_desc(desc: str) -> str:
    """Return 'vip' or 'standard' from a seat content-desc."""
    desc_lower = desc.lower()
    if "vip" in desc_lower:
        return "vip"
    if "standard" in desc_lower:
        return "standard"
    raise ValueError(f"Cannot determine tier from content-desc: {desc!r}")


def save_evidence(data: dict, screenshot_bytes=None):
    """Save JSON evidence and optional screenshot to evidence/ticket-2/."""
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    json_path = os.path.join(EVIDENCE_DIR, "save10-mixed-tiers-evidence.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n[evidence] JSON saved → {json_path}")
    if screenshot_bytes:
        img_path = os.path.join(EVIDENCE_DIR, "payment-screen-save10.png")
        with open(img_path, "wb") as f:
            f.write(screenshot_bytes)
        print(f"[evidence] Screenshot saved → {img_path}")


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------

def test_save10_mixed_tiers():
    options = UiAutomator2Options()
    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)

    try:
        nav = WebDriverWait(driver, NAV_WAIT)

        # ------------------------------------------------------------------
        # 1. Guest entry
        # ------------------------------------------------------------------
        nav.until(
            EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "Continue as Guest")
            )
        ).click()

        # ------------------------------------------------------------------
        # 2. Event list → scroll to Neon Skyline → open it
        # ------------------------------------------------------------------
        wait_for(driver, "event-list-screen")
        nav.until(
            EC.presence_of_element_located(
                (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector().resourceId("event-list")'
                    ".scrollable(true))"
                    f'.scrollIntoView(new UiSelector().resourceId("{EVENT_CARD_ID}"))',
                )
            )
        ).click()

        # ------------------------------------------------------------------
        # 3. Event details → Select a Seat
        # ------------------------------------------------------------------
        wait_for(driver, "select-seat-button").click()

        # ------------------------------------------------------------------
        # 4. Seat selection — read base prices from content-desc, then select
        # ------------------------------------------------------------------
        wait_for(driver, VIP_SEAT_ID)

        vip_elem = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().resourceId("{VIP_SEAT_ID}")',
        )
        vip_desc = vip_elem.get_attribute("content-desc")
        vip_tier = extract_tier_from_content_desc(vip_desc)
        vip_base = extract_price_from_content_desc(vip_desc)
        assert vip_tier == "vip", (
            f"Seat {VIP_SEAT_ID} expected tier 'vip', got {vip_tier!r}. "
            f"content-desc: {vip_desc!r}"
        )
        assert "available" in vip_desc.lower() or "selected" in vip_desc.lower(), (
            f"Seat {VIP_SEAT_ID} is not available. content-desc: {vip_desc!r}"
        )
        vip_elem.click()

        std_elem = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().resourceId("{STD_SEAT_ID}")',
        )
        std_desc = std_elem.get_attribute("content-desc")
        std_tier = extract_tier_from_content_desc(std_desc)
        std_base = extract_price_from_content_desc(std_desc)
        assert std_tier == "standard", (
            f"Seat {STD_SEAT_ID} expected tier 'standard', got {std_tier!r}. "
            f"content-desc: {std_desc!r}"
        )
        assert "available" in std_desc.lower() or "selected" in std_desc.lower(), (
            f"Seat {STD_SEAT_ID} is not available. content-desc: {std_desc!r}"
        )
        std_elem.click()

        print(f"\n[seat prices] VIP base={vip_base}, Standard base={std_base}")

        # Compute PRD-correct expectations from live prices
        expected_discount = (Decimal("0.10") * std_base).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        expected_subtotal = (std_base + vip_base).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        expected_vip_line = vip_base          # no discount on VIP
        expected_std_line = (std_base - expected_discount).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        expected_total = (expected_std_line + vip_base).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        wait_for(driver, "seat-selection-continue-button").click()

        # ------------------------------------------------------------------
        # 5. Discount code screen — dismiss keyboard, enter and apply SAVE10
        # ------------------------------------------------------------------
        wait_for(driver, "discount-screen")
        discount_input = wait_for(driver, "discount-input", timeout=INPUT_WAIT)
        discount_input.clear()
        discount_input.send_keys(DISCOUNT_CODE)

        # Dismiss keyboard so the Apply button is not obscured
        try:
            driver.hide_keyboard()
        except Exception:
            pass

        wait_for(driver, "discount-apply-button", timeout=INPUT_WAIT).click()

        # Wait for the applied label to confirm code was accepted
        WebDriverWait(driver, INPUT_WAIT).until(
            EC.presence_of_element_located(by_id("discount-applied-label"))
        )

        wait_for(driver, "discount-continue-button").click()

        # ------------------------------------------------------------------
        # 6. Payment screen — capture screenshot + raw text BEFORE assertions
        # ------------------------------------------------------------------
        wait_for(driver, "payment-screen")

        # Capture screenshot for evidence
        try:
            screenshot_bytes = driver.get_screenshot_as_png()
        except Exception as e:
            screenshot_bytes = None
            print(f"[warning] Screenshot failed: {e}")

        # Read raw text from each payment element
        vip_line_raw      = wait_for(driver, "payment-line-price-A1", timeout=INPUT_WAIT).text.strip()
        std_line_raw      = wait_for(driver, "payment-line-price-C1", timeout=INPUT_WAIT).text.strip()
        subtotal_raw      = wait_for(driver, "payment-subtotal",       timeout=INPUT_WAIT).text.strip()
        discount_raw      = wait_for(driver, "payment-discount-amount",timeout=INPUT_WAIT).text.strip()
        total_raw         = wait_for(driver, "payment-total",          timeout=INPUT_WAIT).text.strip()

        print(f"\n[payment screen raw values]")
        print(f"  VIP line (A1):      {vip_line_raw!r}")
        print(f"  Standard line (C1): {std_line_raw!r}")
        print(f"  Subtotal:           {subtotal_raw!r}")
        print(f"  Discount:           {discount_raw!r}")
        print(f"  Total:              {total_raw!r}")

        # Parse amounts (parse_price strips sign — is_negative checks sign separately)
        actual_vip_line  = parse_price(vip_line_raw)
        actual_std_line  = parse_price(std_line_raw)
        actual_subtotal  = parse_price(subtotal_raw)
        actual_discount  = parse_price(discount_raw)   # positive magnitude
        actual_total     = parse_price(total_raw)

        # ------------------------------------------------------------------
        # 7. Save evidence JSON + screenshot BEFORE assertions
        # ------------------------------------------------------------------
        evidence = {
            "event": "Neon Skyline (evt-01)",
            "seats": {
                "vip":      {"id": VIP_SEAT_ID, "tier": vip_tier, "base_price": str(vip_base)},
                "standard": {"id": STD_SEAT_ID, "tier": std_tier, "base_price": str(std_base)},
            },
            "discount_code": DISCOUNT_CODE,
            "raw_payment_screen": {
                "vip_line":   vip_line_raw,
                "std_line":   std_line_raw,
                "subtotal":   subtotal_raw,
                "discount":   discount_raw,
                "total":      total_raw,
            },
            "actual": {
                "vip_line_price":  str(actual_vip_line),
                "std_line_price":  str(actual_std_line),
                "subtotal":        str(actual_subtotal),
                "discount_amount": str(actual_discount),
                "discount_is_negative": is_negative(discount_raw),
                "total":           str(actual_total),
            },
            "expected_per_prd": {
                "vip_line_price":  str(expected_vip_line),
                "std_line_price":  str(expected_std_line),
                "subtotal":        str(expected_subtotal),
                "discount_amount": str(expected_discount),
                "total":           str(expected_total),
                "rule": "SAVE10 = 10% off Standard only; VIP must not be discounted",
            },
        }
        save_evidence(evidence, screenshot_bytes)

        # ------------------------------------------------------------------
        # 8. Assertions — collect ALL mismatches, then fail together
        # ------------------------------------------------------------------
        failures = []

        # Discount row must be negative (a deduction)
        if not is_negative(discount_raw):
            failures.append(
                f"Discount row is not negative: raw={discount_raw!r}"
            )

        # VIP seat must NOT be discounted
        if actual_vip_line != expected_vip_line:
            failures.append(
                f"VIP seat A1 was discounted. "
                f"Expected ${expected_vip_line} (no discount), got ${actual_vip_line}. "
                f"PRD: SAVE10 must not discount VIP-tier seats."
            )

        # Standard seat must be discounted by 10%
        if actual_std_line != expected_std_line:
            failures.append(
                f"Standard seat C1 price wrong. "
                f"Expected ${expected_std_line} (0.90 × ${std_base}), got ${actual_std_line}."
            )

        # Subtotal must equal S + V (pre-discount sum)
        if actual_subtotal != expected_subtotal:
            failures.append(
                f"Subtotal wrong. "
                f"Expected ${expected_subtotal} (${std_base} + ${vip_base}), got ${actual_subtotal}."
            )

        # Discount magnitude must equal 10% of Standard only
        if actual_discount != expected_discount:
            failures.append(
                f"Discount amount wrong. "
                f"Expected ${expected_discount} (10% of Standard ${std_base} only), "
                f"got ${actual_discount}. "
                f"PRD: SAVE10 must not discount VIP-tier seats."
            )

        # Final total must be 0.90*S + V
        if actual_total != expected_total:
            failures.append(
                f"Checkout total wrong. "
                f"Expected ${expected_total} (0.90×${std_base} + ${vip_base}), "
                f"got ${actual_total}. "
                f"PRD: SAVE10 applies to Standard only."
            )

        if failures:
            msg = "\n".join(f"  [{i+1}] {f}" for i, f in enumerate(failures))
            pytest.fail(
                f"SAVE10 mixed-tier test FAILED — {len(failures)} violation(s):\n{msg}"
            )

        print("\n[SAVE10 mixed-tier] All assertions PASSED.")

    finally:
        driver.quit()
