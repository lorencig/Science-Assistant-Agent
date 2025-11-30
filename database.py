import sqlite3

def init_db():
    conn = sqlite3.connect("seen_papers.db")
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS seen (id TEXT PRIMARY KEY)')
    conn.commit()
    conn.close()

def is_new(paper_id):
    conn = sqlite3.connect("seen_papers.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM seen WHERE id=?", (paper_id,))
    exists = c.fetchone()
    if not exists:
        c.execute("INSERT INTO seen VALUES (?)", (paper_id,))
        conn.commit()
    conn.close()
    return exists is None