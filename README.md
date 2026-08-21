# livekit-demo

Minimal Google Meet–style video call demo on [LiveKit](https://livekit.io/): a FastAPI token
server plus a React frontend using LiveKit's prebuilt `VideoConference` UI (tile grid, mute,
camera toggle, screen share, participant list).

See [`LiveCall_Implementation_Plan.md`](./LiveCall_Implementation_Plan.md) for the full
production plan (admission workflow, recording, Postgres) this demo scopes down from.

## Setup

Create `server/.env` with your LiveKit Cloud credentials:

```
LIVEKIT_URL=wss://<your-project>.livekit.cloud
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
```

## Run with Docker

```
make up
```

Server: http://localhost:8001, client: http://localhost:5173

## Run locally

```
make install
make dev-server   # terminal 1
make dev-client   # terminal 2
```

## Try it

Open http://localhost:5173 in two browser tabs (or two devices), enter different names with
the same room name, and hit Join.
