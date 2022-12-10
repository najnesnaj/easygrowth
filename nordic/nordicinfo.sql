BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS nordicinfo (
        symbol TEXT PRIMARY KEY,
        name  TEXT,
        currency TEXT,
        sector        TEXT,
        sectorcode    TEXT,
        ISIN      TEXT,
        trailingPE    REAL,
        EPS   REAL,
        analist_estimate REAL,
        Price_book    REAL,
        TangibleValuePerShare REAL,
        enterpriseToEbitda    REAL,
        totalDebt     REAL,
        currentRatio  REAL,
        growthrate    REAL,
        growthrate_quarter REAL,
        beta  REAL,
        priceToSalesTrailing12Months  REAL,
        extrainfo TEXT,
        value_score     REAL,
        risc_score     REAL,
        growth_score   REAL
);

CREATE UNIQUE INDEX "ISIN_index" ON "nordicinfo" ("ISIN");
COMMIT;
