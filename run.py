"""Convenience entry point: `python run.py`"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.presentation.app:app", host="127.0.0.1", port=8000, reload=True)
