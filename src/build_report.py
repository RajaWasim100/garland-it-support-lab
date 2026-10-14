#!/usr/bin/env python3
"""Build aggregate-only support-lab metrics from explicitly fictional CSV records."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TICKET_FIELDS = {"ticket_id", "opened_at", "closed_at", "requester", "asset_tag", "category", "priority", "status", "channel", "summary", "resolution", "minutes_to_resolve", "first_response_minutes", "reopened", "escalated"}
ASSET_FIELDS = {"asset_tag", "asset_type", "model", "serial_stub", "assigned_to", "location", "assigned_date", "warranty_end", "status", "encryption_status", "patch_state", "last_inventory_check"}
LIFECYCLE_FIELDS = {"request_id", "request_type", "request_date", "effective_date", "person", "asset_tag", "manager_approval", "identity_action", "device_action", "access_review", "data_retention", "shipping_tracking", "status", "lab_note"}

def read_csv(path: Path, required: set[str], key: str) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing required fields: {', '.join(sorted(missing))}")
        rows = list(reader)
    seen: set[str] = set()
    for number, row in enumerate(rows, start=2):
        value = (row.get(key) or "").strip()
        if not value:
            raise ValueError(f"{path}:{number}: blank {key}")
        if value in seen:
            raise ValueError(f"{path}:{number}: duplicate {key} {value}")
        seen.add(value)
    return rows

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def parse_time(value: str, path: Path, row_num: int, field: str) -> datetime:
    try:
        result = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{path}:{row_num}: invalid {field} timestamp {value!r}") from exc
    if result.tzinfo is not None:
        raise ValueError(f"{path}:{row_num}: {field} must be timezone-naive local lab time")
    return result

def integer(value: str, path: Path, row_num: int, field: str, *, minimum: int = 0) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{path}:{row_num}: invalid integer {field}={value!r}") from exc
    if parsed < minimum:
        raise ValueError(f"{path}:{row_num}: {field} must be >= {minimum}")
    return parsed

def boolean(value: str, path: Path, row_num: int, field: str) -> bool:
    normalized = value.strip().lower()
    if normalized not in {"true", "false"}:
        raise ValueError(f"{path}:{row_num}: {field} must be true or false")
    return normalized == "true"

def validate_tickets(rows: list[dict[str, str]], path: Path) -> list[dict[str, Any]]:
    clean: list[dict[str, Any]] = []
    for row_num, row in enumerate(rows, start=2):
        opened = parse_time(row["opened_at"], path, row_num, "opened_at")
        closed = parse_time(row["closed_at"], path, row_num, "closed_at")
        if closed < opened:
            raise ValueError(f"{path}:{row_num}: closed_at precedes opened_at")
        minutes = integer(row["minutes_to_resolve"], path, row_num, "minutes_to_resolve")
        first = integer(row["first_response_minutes"], path, row_num, "first_response_minutes")
        actual = int((closed - opened).total_seconds() // 60)
        if actual != minutes:
            raise ValueError(f"{path}:{row_num}: minutes_to_resolve does not match timestamps ({minutes} != {actual})")
        if first > minutes:
            raise ValueError(f"{path}:{row_num}: first response occurs after resolution")
        clean.append({**row, "minutes_to_resolve": minutes, "first_response_minutes": first,
                      "reopened": boolean(row["reopened"], path, row_num, "reopened"),
                      "escalated": boolean(row["escalated"], path, row_num, "escalated")})
    return clean

def create_local_db(path: Path, tickets: list[dict[str, Any]], assets: list[dict[str, str]], lifecycle: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    with sqlite3.connect(path) as db:
        db.executescript("""
        CREATE TABLE tickets(ticket_id TEXT PRIMARY KEY, opened_at TEXT, closed_at TEXT, requester TEXT, asset_tag TEXT, category TEXT, priority TEXT, status TEXT, channel TEXT, summary TEXT, resolution TEXT, minutes_to_resolve INTEGER, first_response_minutes INTEGER, reopened INTEGER, escalated INTEGER);
        CREATE TABLE assets(asset_tag TEXT PRIMARY KEY, asset_type TEXT, model TEXT, serial_stub TEXT, assigned_to TEXT, location TEXT, assigned_date TEXT, warranty_end TEXT, status TEXT, encryption_status TEXT, patch_state TEXT, last_inventory_check TEXT);
        CREATE TABLE lifecycle(request_id TEXT PRIMARY KEY, request_type TEXT, request_date TEXT, effective_date TEXT, person TEXT, asset_tag TEXT, manager_approval TEXT, identity_action TEXT, device_action TEXT, access_review TEXT, data_retention TEXT, shipping_tracking TEXT, status TEXT, lab_note TEXT);
        CREATE INDEX idx_tickets_category ON tickets(category);
        CREATE INDEX idx_tickets_asset ON tickets(asset_tag);
        """)
        db.executemany("INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [tuple(int(r[k]) if k in {"reopened", "escalated"} else int(r[k]) if k in {"minutes_to_resolve", "first_response_minutes"} else r[k] for k in ["ticket_id", "opened_at", "closed_at", "requester", "asset_tag", "category", "priority", "status", "channel", "summary", "resolution", "minutes_to_resolve", "first_response_minutes", "reopened", "escalated"]) for r in tickets])
        db.executemany("INSERT INTO assets VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", [tuple(r[k] for k in ["asset_tag", "asset_type", "model", "serial_stub", "assigned_to", "location", "assigned_date", "warranty_end", "status", "encryption_status", "patch_state", "last_inventory_check"]) for r in assets])
        db.executemany("INSERT INTO lifecycle VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [tuple(r[k] for k in ["request_id", "request_type", "request_date", "effective_date", "person", "asset_tag", "manager_approval", "identity_action", "device_action", "access_review", "data_retention", "shipping_tracking", "status", "lab_note"]) for r in lifecycle])
    # Close here: sqlite3 context managers commit/rollback but do not close the connection.
    db.close()

def build_report(tickets_path: Path, assets_path: Path, lifecycle_path: Path) -> dict[str, Any]:
    tickets = validate_tickets(read_csv(tickets_path, TICKET_FIELDS, "ticket_id"), tickets_path)
    assets = read_csv(assets_path, ASSET_FIELDS, "asset_tag")
    lifecycle = read_csv(lifecycle_path, LIFECYCLE_FIELDS, "request_id")
    ticket_assets = {row["asset_tag"] for row in tickets}
    asset_tags = {row["asset_tag"] for row in assets}
    if not ticket_assets <= asset_tags:
        raise ValueError(f"tickets reference missing assets: {', '.join(sorted(ticket_assets - asset_tags))}")
    categories = Counter(row["category"] for row in tickets)
    priorities = Counter(row["priority"] for row in tickets)
    status = Counter(row["status"] for row in tickets)
    asset_status = Counter(row["status"] for row in assets)
    patch = Counter(row["patch_state"] for row in assets)
    encryption = Counter(row["encryption_status"] for row in assets)
    lifecycle_status = Counter(row["status"] for row in lifecycle)
    lifecycle_type = Counter(row["request_type"] for row in lifecycle)
    resolve_by_category: dict[str, list[int]] = defaultdict(list)
    for row in tickets:
        resolve_by_category[row["category"]].append(row["minutes_to_resolve"])
    return {
        "title": "Windows IT Support & Asset Lifecycle — Simulated Portfolio Lab",
        "notice": "Every person, ticket, asset, event, and tracking reference in this project is fictional. No employer relationship or real support action is represented.",
        "provenance": {"dataset": "Locally authored synthetic lab scenarios", "license": "Project-authored synthetic data", "ticket_source_sha256": sha256(tickets_path), "asset_source_sha256": sha256(assets_path), "lifecycle_source_sha256": sha256(lifecycle_path)},
        "scope": {"tickets": len(tickets), "assets": len(assets), "lifecycle_requests": len(lifecycle), "distinct_assets_with_tickets": len(ticket_assets), "currency": "Not applicable"},
        "ticket_metrics": {"by_category": [{"label": k, "count": v} for k,v in categories.most_common()], "by_priority": [{"label": k, "count": v} for k,v in priorities.most_common()], "by_status": [{"label": k, "count": v} for k,v in status.most_common()], "median_resolution_minutes": median(r["minutes_to_resolve"] for r in tickets), "median_first_response_minutes": median(r["first_response_minutes"] for r in tickets), "reopened_count": sum(r["reopened"] for r in tickets), "escalated_count": sum(r["escalated"] for r in tickets), "resolution_minutes_by_category": [{"label": k, "median_minutes": median(v), "ticket_count": len(v)} for k,v in sorted(resolve_by_category.items())]},
        "asset_metrics": {"by_status": [{"label": k, "count": v} for k,v in asset_status.most_common()], "by_patch_state": [{"label": k, "count": v} for k,v in patch.most_common()], "by_encryption_status": [{"label": k, "count": v} for k,v in encryption.most_common()], "inventory_check_date": max(r["last_inventory_check"] for r in assets)},
        "lifecycle_metrics": {"by_request_type": [{"label": k, "count": v} for k,v in lifecycle_type.most_common()], "by_status": [{"label": k, "count": v} for k,v in lifecycle_status.most_common()], "approval_pending_count": sum(r["manager_approval"].lower() != "approved" for r in lifecycle), "actions_not_executed_count": sum("not executed" in r["identity_action"].lower() or "not executed" in r["device_action"].lower() for r in lifecycle)},
        "data_quality": {"ticket_asset_references_valid": True, "all_ticket_ids_unique": True, "ticket_resolution_durations_match_timestamps": True, "records_are_fictional": True},
        "metric_definitions": {"resolution": "Synthetic elapsed minutes from opened_at to closed_at; simulated examples only, not SLA or employer performance.", "first_response": "Synthetic minutes to first response; not measured service-level attainment.", "escalated": "Scenario flag marking fictional cases routed to a higher support tier or security owner.", "asset": "Fictional asset inventory with stub serials; no real device inventory.", "lifecycle": "Mock approvals and tasks; no live account, license, device, wipe, or shipment action occurred."},
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tickets", type=Path, default=ROOT / "data/tickets.csv")
    parser.add_argument("--assets", type=Path, default=ROOT / "data/assets.csv")
    parser.add_argument("--lifecycle", type=Path, default=ROOT / "data/lifecycle.csv")
    parser.add_argument("--out", type=Path, default=ROOT / "reports/support-summary.json")
    parser.add_argument("--db", type=Path, default=ROOT / "data/processed/support-lab.sqlite")
    args = parser.parse_args()
    report = build_report(args.tickets, args.assets, args.lifecycle)
    create_local_db(args.db, validate_tickets(read_csv(args.tickets, TICKET_FIELDS, "ticket_id"), args.tickets), read_csv(args.assets, ASSET_FIELDS, "asset_tag"), read_csv(args.lifecycle, LIFECYCLE_FIELDS, "request_id"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Built report for {report['scope']['tickets']} fictional tickets and {report['scope']['assets']} fictional assets: {args.out}")

if __name__ == "__main__":
    main()
