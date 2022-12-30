import sqlite3
import pandas as pd

df = pd.read_csv("../currencies_rates.csv", dtype={"date": "str", "USD": "float32", "EUR": "float32",
                                                   "KZT": "float32", "UAH": "float32", "BYR": "float32"})
con = sqlite3.connect("currencies_rates.db")
# cursor = con.cursor()
df.to_sql('CURRENCIES', con, if_exists='append', index=False)
