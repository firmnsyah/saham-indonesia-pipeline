"""Transform: baca data mentah, bersihkan & hitung indikator → data/staging/."""
import glob
import os
import pandas as pd

RAW_DIR = "data/raw"
STAGING_DIR = "data/staging"


def transform():
    os.makedirs(STAGING_DIR, exist_ok=True)

    files = glob.glob(os.path.join(RAW_DIR, "*.csv"))
    if not files:
        print("⚠️  Tidak ada file di data/raw/. Jalankan extract dulu.")
        return

    # 1) Baca tiap CSV + tandai tickernya (dari nama file)
    frames = []
    for path in files:
        ticker = os.path.basename(path).split("_")[0]   # BBCA.JK_2026-...csv → BBCA.JK
        df = pd.read_csv(path)
        df["ticker"] = ticker
        frames.append(df)

    # 2) Gabung semua saham jadi satu tabel
    data = pd.concat(frames, ignore_index=True)

    # 3) Bersihkan: nama kolom kecil, tanggal rapi, pilih kolom penting
    data = data.rename(columns=str.lower)
    data["date"] = pd.to_datetime(data["date"].astype(str).str[:10]).dt.date
    data = data[["date", "ticker", "open", "high", "low", "close", "volume"]]

    # 4) Urutkan per saham menurut tanggal (WAJIB sebelum hitung indikator)
    data = data.sort_values(["ticker", "date"]).reset_index(drop=True)

    # 5) Hitung indikator PER saham
    grup = data.groupby("ticker")
    data["return_harian"] = grup["close"].pct_change() * 100
    data["ma_7"] = grup["close"].transform(lambda s: s.rolling(7).mean())
    data["ma_30"] = grup["close"].transform(lambda s: s.rolling(30).mean())

    # 6) Bulatkan biar rapi
    for c in ["return_harian", "ma_7", "ma_30"]:
        data[c] = data[c].round(2)

    out = os.path.join(STAGING_DIR, "saham_clean.csv")
    data.to_csv(out, index=False)
    print(f"✅ Transform selesai: {len(data)} baris → {out}")
    print("\nContoh 5 baris terakhir:")
    print(data.tail(5).to_string(index=False))


if __name__ == "__main__":
    transform()
