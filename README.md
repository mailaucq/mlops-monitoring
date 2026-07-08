# mlops-monitoring
# Project Setup

This project uses **Python 3.12** and **uv** for dependency management.

## Prerequisites

Install **uv**:

### Linux / macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or install using pip:

```bash
pip install uv
```

Verify the installation:

```bash
uv --version
```

---

## Install Python 3.12

If Python 3.12 is not installed:

```bash
uv python install 3.12
```

Verify:

```bash
uv python list
```

---

## Create a Virtual Environment

Create a virtual environment using Python 3.12:

```bash
uv venv --python 3.12
```

Activate it.

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

---

## Install Dependencies

Install all dependencies from `requirements.txt`:

```bash
uv pip install -r requirements.txt
```

## Running the Drift Tests

Before running the drift detection scripts, generate the synthetic datasets.

### 1. Generate Synthetic Data

```bash
python m01_local_datadrift/01_generate_synthetic_data.py
python m02_local_conceptdrift/01_generate_synthetic_data.py
```

### 2. Run the Data Drift Test

```bash
python m01_local_datadrift/02_evidently_drift_local.py
```

### 3. Run the Target (Concept) Drift Test

```bash
python m02_local_conceptdrift/02_evidently_drift_local.py
```

> **Note:** Always generate the synthetic data before executing the drift tests to ensure the required datasets are available.