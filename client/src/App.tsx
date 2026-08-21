import { useState } from "react";
import "@livekit/components-styles";
import { LiveKitRoom, VideoConference } from "@livekit/components-react";

const TOKEN_ENDPOINT = import.meta.env.VITE_TOKEN_ENDPOINT ?? "http://localhost:8000/api/token";

export default function App() {
  const [room, setRoom] = useState("demo-room");
  const [identity, setIdentity] = useState("");
  const [conn, setConn] = useState<{ token: string; url: string } | null>(null);
  const [error, setError] = useState("");

  async function join() {
    setError("");
    try {
      const res = await fetch(
        `${TOKEN_ENDPOINT}?room=${encodeURIComponent(room)}&identity=${encodeURIComponent(identity)}`,
      );
      if (!res.ok) throw new Error(await res.text());
      setConn(await res.json());
    } catch (e) {
      setError(e instanceof Error ? e.message : "failed to join");
    }
  }

  if (conn) {
    return (
      <LiveKitRoom
        token={conn.token}
        serverUrl={conn.url}
        connect
        video
        audio
        data-lk-theme="default"
        style={{ height: "100vh" }}
        onDisconnected={() => setConn(null)}
      >
        <VideoConference />
      </LiveKitRoom>
    );
  }

  return (
    <div style={{ display: "grid", placeItems: "center", height: "100vh", fontFamily: "sans-serif" }}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          join();
        }}
        style={{ display: "flex", flexDirection: "column", gap: 12, width: 280 }}
      >
        <h1 style={{ margin: 0, fontSize: 20 }}>Join a call</h1>
        <input placeholder="Your name" value={identity} onChange={(e) => setIdentity(e.target.value)} required />
        <input placeholder="Room name" value={room} onChange={(e) => setRoom(e.target.value)} required />
        <button type="submit">Join</button>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </form>
    </div>
  );
}
