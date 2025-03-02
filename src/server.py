import uvicorn
from src.api.app import app

# Direct run without __main__ check
uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info") 