BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "quickfs" (
"Symbol" TEXT,
"Year" INTEGER,
"Revenue" REAL,
"Revenue Growth" REAL,
"Gross Profit" REAL,
"Gross Margin" REAL,
"Operating Profit" REAL,
"Operating Margin" REAL,
"Earnings Per Share" REAL,
"EPS Growth" REAL,
"Return on Assets" REAL,
"Return on Equity" REAL,
"Return on Invested Capital" REAL,
"CUSIP" TEXT,
"ISIN" TEXT,
"Yahoo Symbol" TEXT,
"extra" TEXT
);	
	

COMMIT;
