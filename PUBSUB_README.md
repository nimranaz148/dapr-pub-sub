# Dapr Pub/Sub Example

This is a simple Dapr pub/sub example with a publisher and subscriber.

## Components

1. **Publisher** (`publisher.py`) - Publishes messages to a topic
2. **Subscriber** (`subscriber.py`) - Subscribes to messages from a topic
3. **Pub/Sub Component** (`components/pubsub.yaml`) - Redis-based pub/sub configuration

## Prerequisites

- Dapr CLI installed
- Redis running (Dapr installs Redis by default during `dapr init`)
- Python dependencies installed (`dapr` and `dapr-ext-fastapi`)

## How to Run

**IMPORTANT**: Make sure you're in the `day-1` directory before running these commands!

```bash
cd ~/Desktop/code\ /python-prjs/dapr/day-1
```

### 1. Start the Subscriber

Open a terminal and run:

```bash
dapr run --app-id subscriber --app-port 8001 --dapr-http-port 3501 --resources-path ./components -- python subscriber.py
```

### 2. Start the Publisher

Open another terminal and run:

```bash
dapr run --app-id publisher --dapr-http-port 3500 --resources-path ./components -- python publisher.py
```

## What Happens

1. The publisher sends 10 messages to the "orders" topic
2. The subscriber receives these messages and prints them to the console
3. Messages are routed through Redis (configured in `components/pubsub.yaml`)

## Architecture

```
Publisher → Dapr Sidecar → Redis → Dapr Sidecar → Subscriber
```

Dapr handles all the pub/sub complexity, making your code simple and decoupled.
