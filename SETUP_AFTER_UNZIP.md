# 📦 Setup After Unzipping

## Quick Setup Instructions

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### What Was Removed
- ✅ `node_modules/` - Will be restored with `npm install`
- ✅ `venv/` - Will be restored with `python -m venv venv`
- ✅ `.next/` - Will be rebuilt with `npm run build`
- ✅ `__pycache__/` - Automatically regenerated
- ✅ `*.pyc` - Automatically regenerated

### Quick Start
Use the provided script:
```bash
chmod +x start.sh
./start.sh
```

This will automatically set up both frontend and backend!

