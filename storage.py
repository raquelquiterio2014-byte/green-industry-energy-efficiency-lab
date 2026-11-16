"""Local review audit; records are editable and not tamper-proof."""
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from core import sha256

def init_db(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_utc TEXT NOT NULL,
            reviewer TEXT NOT NULL,
            decision TEXT NOT NULL,
            rationale TEXT NOT NULL,
            input_hash TEXT NOT NULL,
            response_hash TEXT NOT NULL)''')

def save_review(path, reviewer, decision, rationale, data, response):
    if decision not in ('approved', 'needs_revision', 'rejected'):
        raise ValueError('Invalid decision')
    if len(reviewer.strip()) < 2 or len(rationale.strip()) < 5:
        raise ValueError('Reviewer and rationale are required')
    init_db(path)
    with sqlite3.connect(path) as conn:
        conn.execute('''INSERT INTO reviews
            (timestamp_utc, reviewer, decision, rationale, input_hash, response_hash)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (datetime.now(timezone.utc).isoformat(), reviewer.strip(), decision,
             rationale.strip(), sha256(data), sha256(response)))

def get_reviews(path):
    init_db(path)
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(r) for r in conn.execute('SELECT * FROM reviews ORDER BY id DESC')]
