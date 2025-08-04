web: cd backend && uvicorn api:app --host 0.0.0.0 --port $PORT
worker: cd backend && dramatiq run_agent_background 