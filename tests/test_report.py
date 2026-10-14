import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from src.build_report import build_report, create_local_db, read_csv, validate_tickets, TICKET_FIELDS, ASSET_FIELDS, LIFECYCLE_FIELDS

ROOT = Path(__file__).resolve().parents[1]

class ReportTests(unittest.TestCase):
    def test_fictional_fixture_builds_privacy_safe_aggregate_report(self):
        report = build_report(ROOT / 'data/tickets.csv', ROOT / 'data/assets.csv', ROOT / 'data/lifecycle.csv')
        self.assertTrue(report['data_quality']['records_are_fictional'])
        self.assertEqual(report['scope']['tickets'], 30)
        self.assertEqual(report['scope']['assets'], 16)
        self.assertGreater(report['ticket_metrics']['median_resolution_minutes'], 0)
        self.assertEqual(report['lifecycle_metrics']['approval_pending_count'], 1)
        self.assertEqual(report['lifecycle_metrics']['actions_not_executed_count'], 2)
        serialized = json.dumps(report)
        for private in ('LAB-1001', 'Alex Morgan', 'GL-WS-014', 'SYN-00014', 'SHIP-SIM-01'):
            self.assertNotIn(private, serialized)

    def test_local_database_and_reference_sql(self):
        tickets = validate_tickets(read_csv(ROOT/'data/tickets.csv', TICKET_FIELDS, 'ticket_id'), ROOT/'data/tickets.csv')
        assets = read_csv(ROOT/'data/assets.csv', ASSET_FIELDS, 'asset_tag')
        lifecycle = read_csv(ROOT/'data/lifecycle.csv', LIFECYCLE_FIELDS, 'request_id')
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td)/'test.sqlite'
            create_local_db(db_path, tickets, assets, lifecycle)
            db = sqlite3.connect(db_path)
            self.assertEqual(db.execute('select count(*) from tickets').fetchone()[0], 30)
            for query in (ROOT/'sql/analysis.sql').read_text().split(';'):
                query = '\n'.join(line for line in query.splitlines() if not line.lstrip().startswith('--')).strip()
                if query: db.execute(query).fetchall()
            db.close()

    def test_rejects_duplicate_ids_and_invalid_resolution_duration(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'tickets.csv'
            with (ROOT/'data/tickets.csv').open(encoding='utf-8', newline='') as source:
                rows=list(csv.DictReader(source))
            fields=list(rows[0])
            with p.open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows([rows[0],rows[0]])
            with self.assertRaisesRegex(ValueError,'duplicate ticket_id'):
                read_csv(p,TICKET_FIELDS,'ticket_id')
            rows[0]['minutes_to_resolve']='1'
            with p.open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerow(rows[0])
            with self.assertRaisesRegex(ValueError,'does not match timestamps'):
                build_report(p,ROOT/'data/assets.csv',ROOT/'data/lifecycle.csv')

    def test_rejects_ticket_asset_orphan(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'tickets.csv'
            with (ROOT/'data/tickets.csv').open(encoding='utf-8', newline='') as source:
                rows=list(csv.DictReader(source))
            rows[0]['asset_tag']='MISSING-ASSET'
            with p.open('w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            with self.assertRaisesRegex(ValueError,'tickets reference missing assets'):
                build_report(p,ROOT/'data/assets.csv',ROOT/'data/lifecycle.csv')

if __name__ == '__main__':
    unittest.main()
