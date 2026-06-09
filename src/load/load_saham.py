"""Load: muat data bersih dari data/staging/ ke database SQLite (idempoten)."""
import os
import sqlite3
import pandas as pd

STAGING_FILE = "data/staging/saham_clean.csv"
DB_FILE = "data/saham.db"
TABLE = "saham"


def load():
    if not os.path.exists(STAGING_FILE):
        print(f"⚠️  {STAGING_FILE} tidak ada. Jalankan transform dulu.")
        return

    df = pd.read_csv(STAGING_FILE)

    # koneksi ke SQLite — file db dibuat otomatis kalau belum ada
    conn = sqlite3.connect(DB_FILE)
    try:
        # if_exists="replace" → IDEMPOTEN: re-run menghasilkan tabel yang sama,
        # tidak menumpuk duplikat.
        df.to_sql(TABLE, conn, if_exists="replace", index=False)

        jumlah = conn.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
        saham = conn.execute(f"SELECT COUNT(DISTINCT ticker) FROM {TABLE}").fetchone()[0]
        print(f"✅ Load selesai: {jumlah} baris dari {saham} saham → {DB_FILE} (tabel '{TABLE}')")
    finally:
        conn.close()


if __name__ == "__main__":
    load()
