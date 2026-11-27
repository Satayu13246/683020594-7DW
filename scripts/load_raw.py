import sys
from pathlib import Path

import duckdb
con = duckdb.connect("northwind.duckdb")
con.execute("CREATE SCHEMA IF NOT EXISTS raw")
rows = con.execute(
    "SELECT COUNT(*) FROM raw.orders").fetchall()
print(rows)     # [(48,)]
con.close()

# ให้พิมพ์ภาษาไทยได้บน Windows ทุกรุ่น
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "raw_data"
DB_PATH = ROOT / "northwind.duckdb"

SOURCES = {
    "customer": "raw/customer.csv",
    "employees": "raw/employees.csv",
    "products": "raw/products.csv",
    "shippers":"raw/shippers.csv",
    "suppliers":"raw/suppliers.csv",
    # ... employees, suppliers, shippers, products
    "orders": "raw/orders.csv",
    "order_details": "raw/order_details.csv",
    "legacy_orders": "legacy/orders.csv",
    "legacy_order_details":
    "legacy/order_details.csv",
}
con = duckdb.connect(str(DB_PATH))
con.execute("CREATE SCHEMA IF NOT EXISTS raw")
for table, path in SOURCES.items():
    csv_path = DATA_DIR / path
    con.execute(f"""
        CREATE OR REPLACE TABLE raw.{table} AS
        SELECT *
        FROM read_csv('{csv_path.as_posix()}',
        header = true)
""")
n = con.execute(
    f"SELECT COUNT(*) FROM raw.{table}"
).fetchall()[0][0]
print(f"raw.{table} {n} rows")