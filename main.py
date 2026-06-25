from numpy import cross
import pandas as pd
from psrqpy import QueryATNF
from pathlib import Path
from scipy.stats import chi2_contingency

NO_RADIO={"NRAD", "AXP", "XINS"}
PATH=Path("query.pkl")

if not PATH.exists():
	query = QueryATNF(params=['Type','Binary'])
	query.save("query.pkl")
	df = query.pandas
else:
	query = QueryATNF(loadquery='query.pkl')
	df = query.pandas

df['is_binary'] = df["BINARY"].notna().map({True:"Bin",False:"Isolated"})
df['emission'] = df["TYPE"].apply(lambda x: "Radio" if x not in NO_RADIO else "Non Radio")

crosstab = pd.crosstab(df['is_binary'], df['emission'])


chi2, p, dof, expected = chi2_contingency(crosstab)
print(crosstab)
print(f"{chi2=}")
print(f"p-val {p}")
print(f"gl {dof}")
print(f"Expected freq {expected}")
