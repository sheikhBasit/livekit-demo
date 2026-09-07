import { useState, useEffect } from "react";
import "@livekit/components-styles";
import { LiveKitRoom, VideoConference } from "@livekit/components-react";
import { useParams, useNavigate } from "react-router-dom";
import HandRaise from "./HandRaise";

const TOKEN_ENDPOINT = import.meta.env.VITE_TOKEN_ENDPOINT ?? "http://localhost:8000/api/token";

export default function Classroom() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const role = user.role || "student";
  
  const { classId = "demo-class" } = useParams();
  const navigate = useNavigate();
  const [conn, setConn] = useState<{ token: string; url: string } | null>(null);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [participantId, setParticipantId] = useState("");

  async function join() {
    setError("");
    try {
      const res = await fetch(`http://localhost:8001/api/rooms/${encodeURIComponent(classId)}/join`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      
      if (data.status === "admitted") {
        setConn({ token: data.token, url: data.ws_url });
        if (role === "teacher") {
           // Auto-start recording pipeline
           fetch(`http://localhost:8001/api/rooms/${encodeURIComponent(classId)}/start-session`, { headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` },
             method: "POST"
           }).catch(e => console.error("Failed to start session/recording:", e));
        }
      } else if (data.status === "waiting") {
        setStatus("waiting");
        setParticipantId(data.participant_id);
        pollStatus(data.participant_id, classId);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "failed to join");
    }
  }

  async function endClass() {
    if (role === "teacher") {
      try {
        await fetch(`http://localhost:8001/api/rooms/${encodeURIComponent(classId)}/end-session`, { headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` },
          method: "POST"
        });
      } catch (e) {
        console.error("Failed to end session:", e);
      }
    }
    setConn(null);
  }

  async function pollStatus(pid: string, cid: string) {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8001/api/rooms/status/${encodeURIComponent(pid)}?room_id=${encodeURIComponent(cid)}`, {
          headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` }
        });
        const data = await res.json();
        if (data.status === "admitted") {
          clearInterval(interval);
          setConn({ token: data.token, url: data.ws_url });
        } else if (data.status === "denied" || data.status === "left") {
          clearInterval(interval);
          setError("Admission denied or left");
          setStatus("");
        }
      } catch (e) {
        console.error(e);
      }
    }, 2000);
  }

  const [waitingParticipants, setWaitingParticipants] = useState<any[]>([]);

  // Periodically fetch waiting participants for teacher
  useEffect(() => {
    if (role === "teacher" && conn) {
      const interval = setInterval(async () => {
        try {
          const res = await fetch(`http://localhost:8001/api/rooms/${encodeURIComponent(classId)}/waiting`, { headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` } });
          const data = await res.json();
          setWaitingParticipants(data.waiting || []);
        } catch(e) {
          console.error("Failed to fetch waiting list");
        }
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [role, conn, classId]);

  async function admit(participantId: string) {
    try {
      await fetch(`http://localhost:8001/api/rooms/${encodeURIComponent(classId)}/admit/${encodeURIComponent(participantId)}`, { headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` },
        method: "POST"
      });
      // Participant will be removed from waiting list on next poll
    } catch(e) {
      console.error(e);
    }
  }

  if (conn) {
    return (
      <div style={{ display: "flex", height: "100vh" }}>
        <div style={{ flex: 1, position: "relative" }}>
          <LiveKitRoom
            token={conn.token}
            serverUrl={conn.url}
            connect
            video
            audio
            data-lk-theme="default"
            style={{ height: "100%", position: "relative" }}
            onDisconnected={() => setConn(null)}
          >
            <VideoConference />
            <HandRaise role={role} userName={user.name} />
          </LiveKitRoom>
        </div>
        {role === "teacher" && (
          <div style={{ width: 250, borderLeft: "1px solid #ccc", padding: 16, overflowY: "auto", fontFamily: "sans-serif", display: 'flex', flexDirection: 'column' }}>
            <div style={{ flex: 1 }}>
              <h3>Waiting Room</h3>
              {waitingParticipants.length === 0 && <p>No one is waiting.</p>}
              {waitingParticipants.map(p => (
                <div key={p.id} style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
                  <span>{p.name}</span>
                  <button onClick={() => admit(p.id)}>Admit</button>
                </div>
              ))}
            </div>
            <button onClick={endClass} style={{ backgroundColor: '#d32f2f', color: 'white', border: 'none', padding: '12px', cursor: 'pointer', fontWeight: 'bold' }}>End Class</button>
          </div>
        )}
      </div>
    );
  }

  if (status === "waiting") {
    return (
      <div style={{ display: "grid", placeItems: "center", height: "100vh", fontFamily: "sans-serif" }}>
        <h2>Waiting for teacher to admit you...</h2>
      </div>
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
        <h1 style={{ margin: 0, fontSize: 20 }}>Welcome, {user.name}</h1>
        <p style={{ margin: 0, fontSize: 14, color: "#666" }}>Role: {role}</p>
        <p style={{ margin: 0, fontSize: 14, color: "#666" }}>Class: {classId}</p>
        <button type="submit" style={{ padding: 8, cursor: "pointer", backgroundColor: "#007bff", color: "white", border: "none" }}>Join Class</button>
        <button type="button" onClick={() => navigate("/")} style={{ padding: 8, cursor: "pointer", backgroundColor: "#eee", border: "1px solid #ccc" }}>Back to Dashboard</button>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </form>
    </div>
  );
}
