# Dapr Pub/Sub System

A professional implementation of event-driven architecture using Dapr's Pub/Sub building block with Python.

## Overview

This project demonstrates a decoupled, scalable pub/sub messaging system using:
- **Dapr Sidecar** for infrastructure abstraction
- **Redis** as the message broker
- **Python** with FastAPI for the subscriber
- **Dapr Python SDK** for the publisher

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              DAPR PUB/SUB SYSTEM                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────┐        ┌───────────────┐        ┌───────────────┐                  │
│  │  PUBLISHER  │        │  PUBLISHER    │        │   MESSAGE    │                  │
│  │   (Python)  │        │   SIDECAR     │◄───────┤    BROKER    │                  │
│  │             │        │   (Dapr)      │        │    (Redis)   │                  │
│  │ ┌─────────┐ │        │ ┌───────────┐ │        │              │                  │
│  │ │  App    │ │        │ │  Pub/Sub  │ │        │ ┌─────────┐  │                  │
│  │ │  Logic  │ │        │ │ Component │ │        │ │ Channel │  │                  │
│  │ └────┬────┘ │        │ └─────┬─────┘ │        │ │ "orders"│  │                  │
│  │      │      │        │       │       │        │ └────┬────┘  │                  │
│  └──────┼──────┘        └───────┼───────┘        └──────┼───────┘                  │
│         │     HTTP/gRPC          │                      │                           │
│         │    :3500               │                      │                           │
│         │                        │                      │                           │
│         ▼                        │                      ▼                           │
│         │                        │               ┌─────────────┐                   │
│         │                        │               │   DAPR      │                   │
│         │                        │               │   CONTROL   │                   │
│         │                        │               │   PLANE     │                   │
│         │                        │               └─────────────┘                   │
│         │                        │                                                    │
│         │                        │                      │                           │
│         │                        │                      ▼                           │
│         │                        │              ┌───────────────┐                   │
│         │                        │              │  SUBSCRIBER   │                   │
│         │                        │              │    SIDECAR    │                   │
│         │                        │              │    (Dapr)     │                   │
│         │                        │              │ ┌───────────┐ │                   │
│         │                        │              │ │ Pub/Sub   │ │                   │
│         │                        │              │ │ Component │ │                   │
│         │                        │              │ └─────┬─────┘ │                   │
│         │                        │              └───────┼───────┘                   │
│         │                        │                      │                           │
│         │                        │                      │ HTTP                      │
│         │                        │                      │ :8001                     │
│         │                        │                      ▼                           │
│         │                        │              ┌─────────────┐                   │
│         │                        │              │ SUBSCRIBER  │                   │
│         │                        │              │  (FastAPI)  │                   │
│         │                        │              │ ┌─────────┐ │                   │
│         │                        │              │ │  App    │ │                   │
│         │                        │              │ │ Logic  │ │                   │
│         │                        │              │ └─────────┘ │                   │
│         │                        │              └─────────────┘                   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Message Flow

```
┌──────────┐     1. Publish Message     ┌─────────────┐     2. Route to Redis    ┌──────────┐
│Publisher │ ────────────────────────► │ Pub Sidecar │ ────────────────────────► │  Redis   │
│ (App)    │   {"id":1, "msg":"..."}    │   (Dapr)    │   PUB "orders" topic    │  Broker  │
└──────────┘                           └─────────────┘                          └────┬─────┘
                                                                                 │
                                                                                 │ 3. Store & Queue
                                                                                 │
                                                                                 ▼
┌──────────┐     6. Process Message    ┌─────────────┐     4. Pull & Deliver   ┌──────────┐
│Subscriber│ ◄─────────────────────── │ Sub Sidecar │ ◄─────────────────────── │  Redis   │
│ (FastAPI)│     Receive & Handle     │   (Dapr)    │   SUB "orders" topic   │  Broker  │
└──────────┘                           └─────────────┘                          └──────────┘
```

---

## Components & Specifications

| Component | Type | Description |
|-----------|------|-------------|
| **Publisher** | Application | Sends events to the pub/sub system using DaprClient |
| **Subscriber** | Application | Receives and processes events via FastAPI webhooks |
| **Dapr Sidecar** | Runtime | Provides pub/sub abstraction, connects app to broker |
| **Redis** | Infrastructure | Message broker for durable event storage and delivery |
| **Pub/Sub Component** | Configuration | Defines the Redis connection and pub/sub settings |

---

## Package Dependencies

```toml
[project]
name = "dapr-pub-sub"
requires-python = ">=3.8"

[project.dependencies]
# Dapr SDK for Python - Core client library
dapr = "1.16.0"

# Dapr FastAPI Extension - Webhook handling for subscriptions
dapr-ext-fastapi = "1.16.0"

# FastAPI - Modern, fast web framework for building APIs
fastapi = "*"

# Uvicorn - ASGI server for running FastAPI
uvicorn = { extras = ["standard"], version = "*" }
```

### Key Packages Explained

| Package | Purpose | Version |
|---------|---------|---------|
| `dapr` | DaprClient for publishing messages to Dapr sidecar | 1.16.0 |
| `dapr-ext-fastapi` | Decorator-based subscription handling | 1.16.0 |
| `fastapi` | High-performance async web framework | Latest |
| `uvicorn` | ASGI server to serve FastAPI subscriber | Latest |

---

## File Structure

```
dapr-pub-sub/
├── components/
│   └── pubsub.yaml          # Dapr component: Redis pub/sub configuration
├── publisher.py             # Message publisher application
├── subscriber.py            # FastAPI subscriber application
├── pyproject.toml           # Python project dependencies
├── uv.lock                  # Locked dependency versions
└── README.md                # This file
```

---

## Dapr Component Configuration

The pub/sub system is configured in `components/pubsub.yaml`:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub                    # Component identifier used in code
spec:
  type: pubsub.redis             # Redis as the pub/sub implementation
  version: v1
  metadata:
    - name: redisHost
      value: localhost:6379       # Redis connection string
```

---

## How It Works

### 1. **Publisher Application**
```python
from dapr.clients import DaprClient

with DaprClient() as client:
    # Publish message to "orders" topic using "pubsub" component
    client.publish_event(
        pubsub_name='pubsub',
        topic_name='orders',
        data=message
    )
```

### 2. **Dapr Sidecar (Publisher)**
- Receives HTTP/gRPC publish request from app
- Serializes message data
- Routes to configured broker (Redis)
- Handles connection pooling and retries

### 3. **Redis Message Broker**
- Stores messages in topic channels
- Provides message durability
- Handles message ordering
- Supports multiple consumer groups

### 4. **Dapr Sidecar (Subscriber)**
- Polls Redis for new messages
- Deserializes message data
- Converts to HTTP webhook
- Delivers to subscriber app endpoint

### 5. **Subscriber Application**
```python
from dapr.ext.fastapi import DaprApp

@dapr_app.subscribe(pubsub="pubsub", topic="orders")
async def handle_order(event_data):
    # Process incoming message
    print(f"Received: {event_data}")
```

---

## Prerequisites

| Requirement | Command |
|------------|---------|
| Python 3.8+ | `python --version` |
| Dapr CLI | `dapr --version` |
| Dapr Runtime | `dapr init` |
| Redis | Included with `dapr init` |

---

## Quick Start

### 1. Install Dependencies

```bash
pip install dapr dapr-ext-fastapi fastapi uvicorn
# or using uv
uv sync
```

### 2. Start Subscriber (Terminal 1)

```bash
dapr run \
  --app-id subscriber \
  --app-port 8001 \
  --dapr-http-port 3501 \
  --resources-path ./components \
  -- python subscriber.py
```

### 3. Start Publisher (Terminal 2)

```bash
dapr run \
  --app-id publisher \
  --dapr-http-port 3500 \
  --resources-path ./components \
  -- python publisher.py
```

### 4. Observe Output

**Subscriber Terminal:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
Received message: {"id": 0, "message": "Hello from publisher - message 0"}
Received message: {"id": 1, "message": "Hello from publisher - message 1"}
...
```

---

## Dapr Sidecar Flags Explained

| Flag | Purpose | Example |
|------|---------|---------|
| `--app-id` | Unique identifier for the application | `subscriber` |
| `--app-port` | Port where your app listens | `8001` |
| `--dapr-http-port` | Port for Dapr HTTP API | `3501` |
| `--dapr-grpc-port` | Port for Dapr gRPC API | `50001` |
| `--resources-path` | Path to Dapr component configs | `./components` |

---

## Key Benefits

| Benefit | Description |
|---------|-------------|
| **Decoupling** | Publishers don't know about subscribers |
| **Scalability** | Add more subscribers without changing publishers |
| **Broker Independence** | Switch from Redis to RabbitMQ/Kafka via config only |
| **Resilience** | Built-in retries and error handling |
| **Observability** | Dapr provides metrics and tracing |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `error validating resources path` | Ensure you're in the project directory with the `components/` folder |
| Redis connection refused | Run `dapr init` to start Redis container |
| Subscriber not receiving messages | Check `--app-port` matches the FastAPI port |
| Port already in use | Change port numbers in `dapr run` commands |

---

## Resources

- [Dapr Documentation](https://docs.dapr.io/)
- [Pub/Sub Building Block](https://docs.dapr.io/developing-applications/building-blocks/pubsub/)
- [Python SDK](https://github.com/dapr/python-sdk)
- [FastAPI](https://fastapi.tiangolo.com/)

---

## License

MIT License
