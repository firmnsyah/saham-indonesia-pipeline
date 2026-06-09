"""Pipeline saham Indonesia — jalankan extract → transform → load sekaligus."""
from src.extract.extract_saham import extract
from src.transform.transform_saham import transform
from src.load.load_saham import load


def main():
    print("🚀 Pipeline saham mulai\n")

    print("1/3 ── EXTRACT  (ambil data dari yfinance)")
    extract()

    print("\n2/3 ── TRANSFORM  (bersihkan & hitung indikator)")
    transform()

    print("\n3/3 ── LOAD  (simpan ke SQLite)")
    load()

    print("\n✅ Pipeline selesai! Data siap di data/saham.db")


if __name__ == "__main__":
    main()
