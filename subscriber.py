from fastapi import FastAPI, Request
from dapr.ext.fastapi import DaprApp
import json


app = FastAPI()
dapr_app = DaprApp(app)


@dapr_app.subscribe(pubsub="pubsub", topic="orders")
async def orders_subscriber(event_data: dict):
    print(f"Received message: {event_data}")
    return {"success": True}


@app.get("/")
async def root():
    return {"message": "Subscriber service is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
