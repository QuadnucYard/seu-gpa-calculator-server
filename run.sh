# gunicorn main:app -b 0.0.0.0:8000 -w 4 -k uvicorn.workers.UvicornWorker --daemon
gunicorn main:app -c run.py