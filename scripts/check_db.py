import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kunqing.sqlite')

def main():
    if not os.path.exists(DB_PATH):
        print(f"DB not found: {DB_PATH}")
        return
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, student_id, email, password_hash, admin_level, last_login FROM users')
    rows = cur.fetchall()
    conn.close()
    print(f"users count: {len(rows)}")
    for r in rows:
        print(f"id={r[0]} student_id={r[1]} email={r[2]} admin_level={r[4]} last_login={r[5]}\n  hash={r[3][:60]}...")

if __name__ == '__main__':
    main()