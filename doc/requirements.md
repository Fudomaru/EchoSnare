# ESP32 Wi‑Fi Scan Logger — First Requirements

## 1. Purpose

This document defines the **initial, frozen requirements** for the ESP32 Wi‑Fi Scan Logger project.

The goal of this system is to **passively observe the local Wi‑Fi environment over time** and store structured scan data on the device for later extraction and analysis.

This document intentionally limits scope. Anything not listed here is explicitly *out of scope* for the first implementation.

---

## 2. Design Philosophy

* Prefer **clarity over cleverness**
* Prefer **append-only storage** over rewriting
* Prefer **raw data** over interpreted data
* Prefer **boring, durable designs** over feature-rich ones
* Respect **flash wear and power constraints**

This system is designed to survive power loss, reboots, and long runtimes without human intervention.

---

## 3. Hardware & Firmware Assumptions

* Device: **ESP32‑S3**
* Firmware: **MicroPython (ESP32 port)**
* Storage: internal NOR flash (no SD card)
* Filesystem mounted at `/`
* No battery‑backed RTC
* Wi‑Fi supported in STA mode

---

## 4. Execution Model

### Files

* `boot.py`

  * Minimal initialization only
  * No application logic

* `main.py`

  * Contains all runtime logic
  * Runs continuously in a loop

### Runtime Flow

1. Device boots
2. `boot.py` executes
3. `main.py` starts
4. Main loop:

   * Enable Wi‑Fi
   * Perform Wi‑Fi scan
   * Normalize scan data
   * Append results to file
   * Disable Wi‑Fi
   * Sleep until next scan

No REPL interaction is required during normal operation.

---

## 5. Scan Schedule

* **Scan interval:** 30 minutes
* **Scans per day:** 48

Timing is enforced using blocking sleep (`time.sleep`).

No timers, interrupts, or schedulers are used in v0.1.

---

## 6. Data Captured Per Scan

Each Wi‑Fi scan captures the following fields for every visible access point:

| Field     | Description              | Required |
| --------- | ------------------------ | -------- |
| SSID      | Network name             | Yes      |
| BSSID     | Access point MAC address | Yes      |
| RSSI      | Signal strength (dBm)    | Yes      |
| Channel   | RF channel               | Yes      |
| Auth Mode | Security mode (enum)     | Yes      |

Not captured:

* Hidden flag
* Vendor lookup
* IP information
* Connected clients
* Traffic data
* Encryption details beyond auth enum

---

## 7. Auth Mode Handling

* Auth mode is stored as the **raw integer enum** returned by the firmware
* No string mapping is performed during capture
* Enum meaning is documented externally

Rationale:

* Smaller storage footprint
* Firmware‑accurate data
* Interpretation deferred to analysis stage

---

## 8. Timestamping

### Format

* Unix epoch timestamp (seconds)

### Source

* Internal RTC

### Synchronization

* Time is synchronized via **NTP over Wi‑Fi**
* Sync occurs:

  * once per boot
  * optionally once per day

If time sync fails:

* System continues running
* Timestamps may be incorrect but monotonic

No external RTC module is used.

---

## 9. Storage Format

### File Granularity

* **One file per day**

Filename format:

```
YYYY-MM-DD.jsonl
```

### Encoding

* JSON Lines (one JSON object per line)
* Append‑only writes

### Record Schema

Each scan appends exactly one JSON object:

```json
{
  "ts": 1700000000,
  "nets": [
    {
      "b": "aa:bb:cc:dd:ee:ff",
      "s": "FRITZ!Box_7530",
      "r": -67,
      "c": 6,
      "a": 3
    }
  ]
}
```

Key definitions:

| Key    | Meaning          |
| ------ | ---------------- |
| `ts`   | Unix timestamp   |
| `nets` | List of networks |
| `b`    | BSSID            |
| `s`    | SSID             |
| `r`    | RSSI             |
| `c`    | Channel          |
| `a`    | Auth mode enum   |

---

## 10. Flash & Wear Considerations

* Append‑only writes only
* No file rewriting
* ≤48 writes per day
* Rotation policy:

  * keep N days (configurable)
  * delete older files before writing new data

Filesystem longevity is prioritized over data retention.

---

## 11. Data Extraction (Deferred)

* Extraction occurs **once per day**
* Initiated externally (e.g. LXC on Proxmox)
* Transport over Wi‑Fi
* Device acts as server only when extraction is requested

No extraction protocol is implemented in v0.1.

---

## 12. Explicit Non‑Goals

This system does **not**:

* Provide a shell or REPL over Wi‑Fi
* Perform packet sniffing or monitoring
* Collect client or traffic data
* Actively connect to scanned networks
* Guarantee absolute time accuracy
* Optimize storage beyond basic rotation

---

## 13. Versioning

* This document represents **v0.1 requirements**
* Changes must be recorded as new revisions
* Requirements are expected to evolve incrementally

---

## 14. Rationale Summary

This project prioritizes:

* understanding over abstraction
* durability over features
* intentional data collection over hoarding

The system is designed to be small, inspectable, and correct before it is expanded.

