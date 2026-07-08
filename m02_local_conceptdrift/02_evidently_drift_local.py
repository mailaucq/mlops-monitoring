"""Demo 2 · Detección de drift en local con Evidently AI.

Entorno: local (sin Databricks). Requiere `pip install evidently pandas scikit-learn pyarrow`.

Uso:
    python notebooks/02_evidently_drift_local.py

Salida:
    reports/drift.html   — reporte visual interactivo
    reports/drift.json   — reporte estructurado para automatización
"""
from pathlib import Path

import pandas as pd

from monitoring import build_drift_report, save_drift_report, summarize_drift

ROOT = Path(__file__).resolve().parents[0]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"


def main():
    # Requiere haber ejecutado antes: python scripts/generate_synthetic_data.py
    reference = pd.read_parquet(DATA / "reference.parquet")
    current = pd.read_parquet(DATA / "current.parquet")
    reference = reference.drop(columns=["customer_id"])
    current   = current.drop(columns=["customer_id"])

    print(f"Reference: {len(reference):,} filas · Current: {len(current):,} filas")

    report = build_drift_report(reference, current)
    html_path, json_path = save_drift_report(report, REPORTS)

    print(f"\n✓ Reporte HTML: {html_path}")
    print(f"✓ Reporte JSON: {json_path}")

    summary = summarize_drift(json_path)
    print("\nResumen de drift:")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    if summary["share_drifted"] > 0.5:
        print(
            "\n⚠️  Más de la mitad de las features tienen drift — considerar reentrenamiento."
        )


if __name__ == "__main__":
    main()
