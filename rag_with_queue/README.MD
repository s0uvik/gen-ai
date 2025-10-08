uv run uvicorn rag_with_queue.server:app --reload
uv run rq worker --with-scheduler --worker-class rq.worker.SimpleWorker
