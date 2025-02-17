# GEN AI SSE

## 1. Installation
### 1.1. Activate the virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 1.2. Install all required packages
```bash
pip install -r requirements.txt
```


## 2. Run the service
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000 --workers 4
```
