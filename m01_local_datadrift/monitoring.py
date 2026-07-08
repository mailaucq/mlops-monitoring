"""Utilidades de monitoreo (drift) para uso local y en Databricks."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def build_drift_report(reference_df: pd.DataFrame, current_df: pd.DataFrame) -> Any:
    """Construye un reporte de drift con Evidently.

    Devuelve el objeto Report (con métricas + presets) ya ejecutado.
    """
    from evidently.metric_preset import DataDriftPreset
    from evidently.report import Report

    metrics = [DataDriftPreset()]
    report = Report(metrics=metrics)
    report.run(reference_data=reference_df, current_data=current_df)
    return report


def save_drift_report(report: Any, output_dir: str | Path) -> tuple[Path, Path]:
    """Guarda el reporte como HTML + JSON. Devuelve rutas de ambos."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    html = out / "drift.html"
    js = out / "drift.json"
    report.save_html(str(html))
    report.save_json(str(js))
    return html, js


def summarize_drift(report_json_path: str | Path) -> dict:
    """Extrae del JSON un resumen: número de features con drift + score global."""
    import json

    with open(report_json_path) as f:
        data = json.load(f)

    n_drifted = 0
    n_features = 0
    for metric in data.get("metrics", []):
        result = metric.get("result", {})
        if "number_of_drifted_columns" in result:
            n_drifted = result["number_of_drifted_columns"]
            n_features = result.get("number_of_columns", 0)

    return {
        "features_drifted": n_drifted,
        "features_total": n_features,
        "share_drifted": (n_drifted / n_features) if n_features else 0.0,
    }
