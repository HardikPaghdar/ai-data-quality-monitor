# AI Data Quality Monitor

A lightweight CSV profiler for spotting common data issues before a dataset reaches a dashboard or downstream pipeline.

## Checks included
- Empty values by required column.
- Missing required columns.
- Exact duplicate rows.
- Numeric summaries and conservative median-absolute-deviation outlier candidates.
- JSON-serializable report output suitable for a CI check or scheduled job.

## Run
Requires Python 3.10+.

```bash
python - <<'PY'
from app import profile_csv
import json
print(json.dumps(profile_csv("examples/customers.csv", ["customer_id", "region", "monthly_spend"]), indent=2))
PY
```

## Tests
`python -m unittest discover -s tests -v`

## Notes
Outliers are candidates for review, not automatically bad records. The MAD rule skips classification when the median absolute deviation is zero. This is a local CSV tool, not a hosted monitoring service; add dataset versioning, PII controls, alert delivery, and contract-specific thresholds before production use.
