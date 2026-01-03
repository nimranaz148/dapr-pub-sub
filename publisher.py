import asyncio
import json
from dapr.clients import DaprClient


async def publish_messages():
    with DaprClient() as client:
        for i in range(10):
            message = {"id": i, "message": f"Hello from publisher - message {i}"}

            # Publish message to topic
            client.publish_event(
                pubsub_name="pubsub",
                topic_name="orders",
                data=json.dumps(message),
                data_content_type="application/json"
            )

            print(f"Published: {message}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(publish_messages())
