# saham-indonesia

Project Data Engineering.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # lalu isi nilainya
```

## Menjalankan
```bash
python main.py
```

## Struktur
- `src/extract`  — ambil data (API, DB, file)
- `src/transform`— bersihkan & olah data
- `src/load`     — simpan ke warehouse/DB
- `data/{raw,staging,processed}` — data per tahap kematangan
- `sql/`  — query & DDL
- `dags/` — Airflow DAG
- `tests/`— unit test
