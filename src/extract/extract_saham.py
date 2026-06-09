"""Extract: ambil harga saham IDX dari yfinance, simpan mentah ke data/raw/."""
import os
from datetime import datetime
import yfinance as yf

# Saham blue-chip IDX. Akhiran .JK = bursa Jakarta (IDX)
TICKERS = ["BBCA.JK", "BBRI.JK", "BMRI.JK", "TLKM.JK", "ASII.JK"]
RAW_DIR = "data/raw"


def extract(period: str = "3mo"):
    """Ambil data OHLC harian tiap saham, simpan 1 CSV per saham (bronze layer)."""
    os.makedirs(RAW_DIR, exist_ok=True)
    tanggal = datetime.now().strftime("%Y-%m-%d")

    for ticker in TICKERS:
        df = yf.Ticker(ticker).history(period=period, interval="1d")
        if df.empty:
            print(f"⚠️  {ticker}: kosong (mungkin kena rate-limit Yahoo) — coba lagi nanti")
            continue
        path = os.path.join(RAW_DIR, f"{ticker}_{tanggal}.csv")
        df.to_csv(path)
        print(f"✅ {ticker}: {len(df)} baris → {path}")


if __name__ == "__main__":
    extract()
