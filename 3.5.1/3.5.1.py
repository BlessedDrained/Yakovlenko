import sqlite3
import pandas as pd

pd.set_option("expand_frame_repr", False)

df = pd.read_csv("cb_currencies.csv")
con = sqlite3.connect("cb_currencies.db")
cur = con.cursor()
df.to_sql("cb_currencies.cb", con, if_exists="replace")