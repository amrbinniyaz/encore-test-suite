# Ticket 3 — Equivalent event times use different clock formats

**Recommended severity: Minor. Call: Ship it with a workaround.** The observed difference is cosmetic: Android 11 shows a 24-hour time, while the other three devices show an equivalent 12-hour time with PM. For this release, accept both equivalent displays and clarify to users/support that 19:30 means 7:30 PM. This is an interpretation/support workaround, not a tested settings change. Standardizing formatting can follow as a low-priority improvement. These are our recommendations, not an organizer-confirmed answer.

## What we observed

The original `test_event_date_display.py` ran unchanged through Test Companion and the BrowserStack SDK against the frozen Encore APK. All four tests passed. BrowserStack build **Encore Hackathon - Ticket 3 #3** contains four test results and four device sessions; build duration 32.99 seconds. Sessions started at 00:59:18 BST on 25 September 2026 (23:59:18 UTC on 24 September).

All devices opened **Neon Skyline**, event `evt-01`, at Riverside Arena. The visible event date was Thursday, 22 October 2026 on all four. The time was semantically 19:30 on all four. Screenshots show complete date/time text and the Select a Seat button, with no date clipping. This test stops on Event Details; it does not prove successful checkout on these devices.

| Coverage | Device | Android | Actual rendered date/time | Public session | Screenshot |
|---|---|---|---|---|---|
| Android 11 phone | Samsung Galaxy S21 | 11.0 | Thu, Oct 22, 2026 · 19:30 | [Open session](https://app-automate.browserstack.com/projects/Encore+Hackathon/builds/Encore+Hackathon+Ticket/3?tab=sessions&public_token=6cf685aea634b4e545fb43be189adc6ff942e0be217c6e85ca9a4b927dbc4e20&details=abc40169f1d9904c944a3ee92a080a552ab46a19) | [View](s21-android11.jpeg) |
| Recent Android phone | Samsung Galaxy S24 | 14.0 | Thu, Oct 22, 2026 · 7:30 PM | [Open session](https://app-automate.browserstack.com/projects/Encore+Hackathon/builds/Encore+Hackathon+Ticket/3?tab=sessions&public_token=6cf685aea634b4e545fb43be189adc6ff942e0be217c6e85ca9a4b927dbc4e20&details=c1efc8faedfa3c23cd75d36bcbec468a36aa37eb) | [View](s24-android14.jpeg) |
| Tablet | Samsung Galaxy Tab S10 Plus | 15.0 | Thu, Oct 22, 2026 · 7:30 PM | [Open session](https://app-automate.browserstack.com/projects/Encore+Hackathon/builds/Encore+Hackathon+Ticket/3?tab=sessions&public_token=6cf685aea634b4e545fb43be189adc6ff942e0be217c6e85ca9a4b927dbc4e20&details=fd9422dc29d0b4b30a2252007831299488843bc3) | [View](tab-s10-android15.jpeg) |
| Different manufacturer phone | Google Pixel 8 | 14.0 | Thu, Oct 22, 2026 · 7:30 PM | [Open session](https://app-automate.browserstack.com/projects/Encore+Hackathon/builds/Encore+Hackathon+Ticket/3?tab=sessions&public_token=6cf685aea634b4e545fb43be189adc6ff942e0be217c6e85ca9a4b927dbc4e20&details=c55179b3470d28fa047a1cc600e28cb659fbf4a2) | [View](pixel8-android14.jpeg) |

All four public session links were opened in Chrome Incognito without signing in on 25 September 2026. The individual session panels and date responses were accessible in public view-only mode. Original visual-log screenshots are also saved here so the evidence remains available independently of the dashboard.

## Why this needs human review

The supplied test only asserts that `event-details-date` is nonempty. Its four passing results establish that text was rendered, not that the dates match or use a particular format. We compared each session's `Get text` response and its Event Details screenshot. The newer devices' printed output includes a narrow no-break space (`U+202F`) before PM; that is formatting, not a different time.

The pattern is consistent with different platform date/time formatting behavior or locale/hour-cycle defaults. **The precise cause is unconfirmed:** no locale, timezone, or 12/24-hour preference was requested in the runtime configuration, and those settings were not exposed in the captured session capability responses. Consequently we cannot isolate Android version as the cause. We did not observe a shifted date, a shifted clock time, or unreadable date text. The app's relative event dates should not be hardcoded to October 22 in future tests.

## Reproduction and integrity

Run from this repository's `python` directory using the existing pinned dependencies:

```sh
BROWSERSTACK_CONFIG_FILE=browserstack.ticket3.local.yml .venv/bin/browserstack-sdk pytest tests/test_event_date_display.py -v -rP
```

The local YAML retains private credentials and the uploaded frozen app ID, selects the four devices above, and enables `debug: true`, `video: true`, and `deviceLogs: true`. It is gitignored. `-rP` preserves captured stdout from passing tests. Locale, timezone, and hour-cycle were left unspecified.

Original script SHA-256 before and after execution: `ef72791756d417b237f9b5b237a67f92e305063fe41630bceaa30c063baeb658`. [Supplied script](../../python/tests/test_event_date_display.py). [Machine-readable results](device-results.json).

## Submission text

> Encore displays Neon Skyline's time as 19:30 on Samsung Galaxy S21/Android 11 and 7:30 PM on Samsung Galaxy S24/Android 14, Galaxy Tab S10 Plus/Android 15, and Google Pixel 8/Android 14. All show Thursday, October 22, 2026, so the observed difference is clock formatting rather than a different event time. Platform formatting or locale/hour-cycle defaults are plausible causes; device preferences were not recorded, so the exact cause remains unconfirmed. Severity: Minor. Call: Ship it with a workaround—accept both equivalent formats and clarify the 24-hour display while formatting is standardized later. All four unchanged-script runs passed; their nonempty-text assertion alone would not detect this difference.

The team submission form has not been submitted.
