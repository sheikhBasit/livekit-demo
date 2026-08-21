# Live Call — Implementation Plan

Wiring the demo (mock tiles + client-side recording) into a real multi-party classroom on LiveKit, on your existing zero-cost stack (Oracle ARM VM, Postgres, Cloudflare R2).

---

## 1. Architecture

```
Student/Teacher Browser (React)
        │  1. request join token
        ▼
FastAPI on Oracle VM  ──────────────►  Postgres (rooms, sessions, recordings)
        │  2. signed JWT
        ▼
LiveKit Cloud (WebRTC SFU, free tier)
        │  3. audio/video/data over WebRTC
        ▼
Browser ◄──────────► Browser  (teacher ↔ students, room-relayed)
        │
        │  4. on room start → Egress API call
        ▼
LiveKit Egress  ──► composite MP4  ──► Cloudflare R2 (recording storage)
        │
        ▼
Postgres row: recordings(room_id, r2_key, duration, started_at)
```

Nothing runs on your VM except the token server and admission/permission logic. LiveKit Cloud handles the actual media relay and recording compositing — that's the part raw WebRTC would've made you build yourself.

---

## 2. Data model additions

```
rooms
  id                uuid pk
  teacher_id        uuid fk -> users
  class_id          uuid fk -> classes
  livekit_room_name text unique      -- permanent, derived from class_id
  created_at        timestamptz

room_sessions
  id                uuid pk
  room_id           uuid fk -> rooms
  started_at        timestamptz
  ended_at          timestamptz null
  egress_id         text null        -- LiveKit egress job id

participants
  id                uuid pk
  session_id        uuid fk -> room_sessions
  user_id           uuid fk -> users
  role              enum('teacher','student')
  status            enum('waiting','admitted','denied','left')
  joined_at         timestamptz null

recordings
  id                uuid pk
  session_id        uuid fk -> room_sessions
  r2_key            text
  duration_seconds  int
  file_size_bytes   bigint
  created_at        timestamptz
```

`livekit_room_name` is generated once per class and never changes — this is what gives you the "permanent meeting ID" behavior from the SOW without any scheduling logic.

---

## 3. Backend (FastAPI on Oracle VM)

### 3.1 Token endpoint
```
POST /api/rooms/{class_id}/join
  → verifies caller's session/JWT (your existing auth)
  → looks up or creates the `rooms` row for class_id
  → if role == student: insert participants row with status='waiting', return {status: "waiting"}
  → if role == teacher: mint LiveKit access token, return {token, ws_url}
```
Uses `livekit-server-sdk` (Python) — `AccessToken` with grants scoped by role:
- **teacher grant:** `roomAdmin: true`, `canPublish: true`, `canSubscribe: true`, `roomRecord: true`
- **student grant:** `roomAdmin: false`, `canPublish: true` (audio only — no `canPublishData` chat), `canSubscribe: true`

This is where the platform rules actually get enforced — not in the frontend. A student token literally cannot open the admin chat channel or mute another participant, no matter what the UI shows.

### 3.2 Admission flow
Student calls join → sits in `waiting` in Postgres, **does not get a LiveKit token yet**. Teacher's client subscribes to a lightweight polling or websocket endpoint (`GET /api/rooms/{id}/waiting`) showing pending participants. On admit:
```
POST /api/rooms/{id}/admit/{participant_id}
  → update status='admitted'
  → mint LiveKit token for that student
  → push it to them (websocket, or student polls /api/rooms/{id}/status)
```

### 3.3 Recording lifecycle
```
POST /api/rooms/{id}/start-session   (called when teacher's token is minted)
  → create room_sessions row
  → call LiveKit Egress API: RoomCompositeEgress
      - output: uploads directly to R2 (S3-compatible, LiveKit supports S3 output natively)
      - layout: "speaker" or "grid"
  → store egress_id

POST /api/rooms/{id}/end-session     (called on "End class")
  → call LiveKit StopEgress(egress_id)
  → mark room_sessions.ended_at
  → LiveKit's egress-ended webhook fires → write recordings row with r2_key, duration, size
```
Because Egress is started server-side when the session starts and only the server can stop it, there is no client-side "pause recording" button to build — the constraint is structural, not just a disabled UI button like in the demo.

### 3.4 Webhooks
Register a LiveKit webhook endpoint (`POST /api/livekit/webhook`) for `egress_ended`, `participant_left`, `room_finished` — keeps Postgres in sync without polling LiveKit.

---

## 4. Frontend integration

Replace demo internals, keep the UI shell:

```
npm i livekit-client @livekit/components-react
```

- Swap each mock `<Avatar>` tile for LiveKit's `<ParticipantTile>` / `<VideoTrack>`, driven by `useTracks()` from `@livekit/components-react`.
- Wrap the whole call screen in `<LiveKitRoom token={token} serverUrl={LIVEKIT_URL} connect={true}>`.
- Mic mute button calls `localParticipant.setMicrophoneEnabled(bool)` instead of toggling a raw MediaStream track.
- Screen share button calls `localParticipant.setScreenShareEnabled(bool)` — LiveKit handles the `getDisplayMedia` call and publishes it as a track automatically, visible to all participants (not just local, like the demo).
- Raise-hand and chat-with-admin: LiveKit **data channels** (`localParticipant.publishData()`), consumed via `useDataChannel()`. No separate backend needed for these — they ride the same WebRTC connection.
- Waiting-room / admitted list: driven by your `/api/rooms/{id}/waiting` endpoint + Postgres, not LiveKit state — LiveKit doesn't know about your admission concept.

---

## 5. Mapping SOW rules to enforcement points

| Rule | Where it's enforced |
|---|---|
| Permanent meeting ID, no scheduling | `rooms.livekit_room_name` fixed at class creation |
| Teacher admits/denies before join | Postgres `participants.status`, gates token issuance |
| Recording always on, teacher can't pause | Server starts/stops Egress; no client API exposed for it |
| No chat for students | Student LiveKit token omits data-publish grant to admin channel; server-side, not just hidden UI |
| Teacher chats only with admin | Separate data channel/topic scoped by role in the token grants |
| Screen share (teacher) | `setScreenShareEnabled`, gated by `canPublish` grant on teacher token only |

---

## 6. Deployment steps on your Oracle VM

1. `pip install livekit-server-sdk livekit-api` in the FastAPI service.
2. Add `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `LIVEKIT_URL` to your env config (per your `app-manifest.yaml` convention).
3. Configure LiveKit Cloud project's Egress output to your R2 bucket (S3-compatible credentials — R2 access key/secret, endpoint, bucket name).
4. Add the webhook URL in LiveKit Cloud dashboard pointing to your VM's public endpoint (needs HTTPS — reuse whatever reverse proxy/Caddy setup you're already running for other services).
5. Add the two new tables + `recordings` to your existing migration flow.

---

## 7. Testing checklist

- [ ] Two browser tabs (different accounts) can join the same permanent room
- [ ] Student join is held in `waiting` until teacher admits
- [ ] Denied/removed student's token is revoked (test they actually get disconnected, not just hidden in UI)
- [ ] Recording starts within a few seconds of teacher joining, without any client action
- [ ] Recording continues correctly through a student join/leave mid-class
- [ ] Ending class stops Egress and a playable file lands in R2 within expected time
- [ ] Student token cannot publish to admin chat channel (test by crafting a raw data-channel call from devtools, not just via UI)
- [ ] Screen share track is visible to all connected participants, not just the sharer

---

## 8. Rough effort estimate

| Piece | Effort |
|---|---|
| Token server + admission endpoints | 1–2 days |
| Postgres schema + migrations | 0.5 day |
| Egress + R2 wiring + webhook | 1 day |
| Frontend LiveKit integration (swap demo internals) | 1–2 days |
| Data-channel chat/raise-hand | 0.5 day |
| End-to-end testing across 2+ real accounts | 1 day |

**Total: ~5–7 focused days** to go from this demo to a working multi-party classroom on your existing infra.
