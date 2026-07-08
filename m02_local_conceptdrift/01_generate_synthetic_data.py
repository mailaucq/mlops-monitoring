"""Genera datasets sintéticos de churn: reference (baseline) y current (con drift artificial).

Uso:
    python scripts/generate_synthetic_data.py

Salida:
    data/reference.parquet   — dataset baseline (para entrenar y como referencia de drift)
    data/current.parquet     — dataset con drift artificial (para las demos de monitoreo)
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
CONTRACT_TYPES = ["month-to-month", "one-year", "two-year"]
PAYMENT_METHODS = ["credit_card", "bank_transfer", "electronic_check", "mailed_check"]
REGIONS = ["north", "south", "east", "west", "center"]


def _make_dataset(n: int, *, drift: bool = False) -> pd.DataFrame:
    tenure = RNG.integers(1, 72, n)

    monthly_charges_base = RNG.normal(70, 25, n).clip(15, 200)
    monthly_charges = monthly_charges_base + 10

    total_charges = monthly_charges * tenure * RNG.uniform(0.9, 1.1, n)
    num_products = RNG.integers(1, 6, n)
    support_tickets = RNG.poisson(1.5, n)
    logins = RNG.poisson(15, n)
    session = RNG.gamma(2, 5, n).clip(0.5, 60)

    contract = RNG.choice(
        CONTRACT_TYPES,
        n,
        p=[0.5, 0.3, 0.2],
    )
    payment = RNG.choice(PAYMENT_METHODS, n)
    region = RNG.choice(REGIONS, n, p=[0.25, 0.25, 0.2, 0.15, 0.15])

    # Probabilidad de churn dependiente de features (relación estable)
    logit = (
        -2.0
        + (0.03 if not drift else 0.06)* (72 - tenure)
        + 0.4 * (contract == "month-to-month")
        + (0.02 if not drift else 0.04) * monthly_charges # drift 
        + (0.3 if not drift else 0.1) * support_tickets # drift
        - 0.05 * logins
    )
    p_churn = 1 / (1 + np.exp(-logit))
    churn = (RNG.uniform(0, 1, n) < p_churn).astype(int)

    return pd.DataFrame(
        {
            "customer_id": [f"C{100000 + i}" for i in range(n)],
            "tenure_months": tenure,
            "monthly_charges": monthly_charges.round(2),
            "total_charges": total_charges.round(2),
            "num_products": num_products,
            "support_tickets_90d": support_tickets,
            "logins_30d": logins,
            "avg_session_minutes": session.round(2),
            "contract_type": contract,
            "payment_method": payment,
            "region": region,
            "churn": churn,
        }
    )


def main():
    data_dir = Path(__file__).resolve().parents[0] / "data"
    data_dir.mkdir(exist_ok=True)

    reference = _make_dataset(5_000, drift=False)
    current = _make_dataset(2_000, drift=True)

    ref_path = data_dir / "reference.parquet"
    cur_path = data_dir / "current.parquet"
    reference.to_parquet(ref_path, index=False)
    current.to_parquet(cur_path, index=False)

    print(f"✓ {ref_path}  ({len(reference):,} filas, {reference['churn'].mean():.1%} churn)")
    print(f"✓ {cur_path}  ({len(current):,} filas, {current['churn'].mean():.1%} churn)")


if __name__ == "__main__":
    main()
