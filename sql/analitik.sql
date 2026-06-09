-- ===========================================================
-- Analitik saham — query untuk database data/saham.db (tabel: saham)
-- Kolom: date, ticker, open, high, low, close, volume,
--        return_harian, ma_7, ma_30
-- ===========================================================

-- 1) Harga & indikator TERBARU tiap saham
SELECT ticker, date, close, ma_7, ma_30, return_harian
FROM saham
WHERE date = (SELECT MAX(date) FROM saham)
ORDER BY ticker;

-- 2) TOP GAINER hari terakhir (kenaikan harian tertinggi)
SELECT ticker, date, close, return_harian
FROM saham
WHERE date = (SELECT MAX(date) FROM saham)
ORDER BY return_harian DESC
LIMIT 3;

-- 3) Saham TREN NAIK: harga di atas rata-rata 30 hari (sinyal bullish)
SELECT ticker, close, ma_30, ROUND(close - ma_30, 2) AS selisih
FROM saham
WHERE date = (SELECT MAX(date) FROM saham)
  AND close > ma_30
ORDER BY selisih DESC;

-- 4) Return rata-rata, hari terbaik & terburuk per saham
SELECT ticker,
       ROUND(AVG(return_harian), 3) AS avg_return,
       ROUND(MAX(return_harian), 2) AS hari_terbaik,
       ROUND(MIN(return_harian), 2) AS hari_terburuk
FROM saham
GROUP BY ticker
ORDER BY avg_return DESC;

-- 5) Momentum: MA-7 vs MA-30
SELECT ticker, ma_7, ma_30,
       CASE WHEN ma_7 > ma_30 THEN 'naik' ELSE 'turun' END AS momentum
FROM saham
WHERE date = (SELECT MAX(date) FROM saham)
ORDER BY ticker;
