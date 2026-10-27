"""Small CSV data-quality profiler with deterministic checks."""
import csv
from pathlib import Path
from statistics import median

def profile_rows(rows: list[dict[str,str]], required_columns: list[str] | None = None) -> dict:
    if not rows: raise ValueError("dataset must contain at least one row")
    columns=list(dict.fromkeys(key for row in rows for key in row.keys()))
    required=required_columns or columns
    missing={col:sum(1 for row in rows if not str(row.get(col,"")).strip()) for col in required}
    duplicate_count=len(rows)-len({tuple(sorted(row.items())) for row in rows})
    issues=[]
    for col,count in missing.items():
        if count: issues.append({"type":"missing_values","column":col,"count":count})
    if duplicate_count: issues.append({"type":"duplicate_rows","count":duplicate_count})
    absent=[col for col in required if col not in columns]
    if absent: issues.append({"type":"missing_columns","columns":absent})
    numeric={}
    for col in columns:
        values=[]
        for row in rows:
            try:
                value=float(row.get(col,""))
                if value==value and abs(value)!=float("inf"): values.append(value)
            except (ValueError,TypeError): pass
        if values and len(values)>=max(3,int(len(rows)*.5)):
            med=median(values); mad=median([abs(v-med) for v in values])
            outliers=[v for v in values if mad>0 and abs(v-med)>3*1.4826*mad]
            numeric[col]={"valid_numeric_values":len(values),"median":med,"robust_outlier_candidates":outliers}
            if outliers: issues.append({"type":"outlier_candidates","column":col,"values":outliers})
    return {"row_count":len(rows),"columns":columns,"missing_cells":missing,"duplicate_rows":duplicate_count,"numeric_summary":numeric,"issues":issues}
def profile_csv(path: str | Path, required_columns: list[str] | None = None) -> dict:
    with open(path,newline="",encoding="utf-8-sig") as handle: rows=list(csv.DictReader(handle))
    return profile_rows(rows,required_columns)
