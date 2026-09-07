import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Dashboard() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "{}");
  const token = localStorage.getItem("token");

  const [activeSessions, setActiveSessions] = useState<any[]>([]);
  const [recordings, setRecordings] = useState<any[]>([]);
  const [teacherHistory, setTeacherHistory] = useState<any[]>([]);

  useEffect(() => {
    if (user.role === 'admin') {
      fetch("http://localhost:8001/api/admin/active-sessions", {
        headers: { "Authorization": `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => setActiveSessions(data.sessions || []))
        .catch(console.error);

      fetch("http://localhost:8001/api/admin/recordings", {
        headers: { "Authorization": `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => setRecordings(data.recordings || []))
        .catch(console.error);
    }
    
    if (user.role === 'teacher') {
      fetch("http://localhost:8001/api/teacher/history", {
        headers: { "Authorization": `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(data => setTeacherHistory(data.history || []))
        .catch(console.error);
    }
  }, [user.role, token]);

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  if (!user.role) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ fontFamily: "sans-serif", padding: 24, maxWidth: 800, margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #ccc", paddingBottom: 16, marginBottom: 24 }}>
        <h1>{user.role.charAt(0).toUpperCase() + user.role.slice(1)} Dashboard</h1>
        <div>
          <span style={{ marginRight: 16 }}>Welcome, {user.name}</span>
          <button onClick={logout} style={{ padding: "8px 16px", cursor: "pointer", backgroundColor: "#eee", border: "1px solid #ccc" }}>Logout</button>
        </div>
      </div>

      {user.role === 'admin' && (
        <div>
          <h2>Platform Administration</h2>
          <div style={{ display: "grid", gap: 16, gridTemplateColumns: "1fr 1fr" }}>
            <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, backgroundColor: "#f9f9f9" }}>
              <h3>Manage Users</h3>
              <p>Create and edit teacher and student accounts.</p>
              <button onClick={() => navigate("/admin/users")} style={{ padding: "8px 16px", cursor: "pointer", backgroundColor: "#007bff", color: "white", border: "none" }}>Go to Users</button>
            </div>
            <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, backgroundColor: "#eef2ff" }}>
              <h3>Live Sessions Wall</h3>
              {activeSessions.length === 0 ? <p>No active classes right now.</p> : (
                <ul style={{ paddingLeft: 20 }}>
                  {activeSessions.map(s => (
                    <li key={s.id}>{s.teacher_name}'s Class (Started: {new Date(s.started_at).toLocaleTimeString()})</li>
                  ))}
                </ul>
              )}
            </div>
            <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, backgroundColor: "#f0fdf4", gridColumn: "1 / -1" }}>
              <h3>Recording Library</h3>
              {recordings.length === 0 ? <p>No recordings found.</p> : (
                <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
                  <thead>
                    <tr style={{ borderBottom: "1px solid #ccc" }}>
                      <th style={{ padding: 8 }}>Teacher</th>
                      <th style={{ padding: 8 }}>Date</th>
                      <th style={{ padding: 8 }}>Duration</th>
                      <th style={{ padding: 8 }}>File</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recordings.map(r => (
                      <tr key={r.id} style={{ borderBottom: "1px solid #eee" }}>
                        <td style={{ padding: 8 }}>{r.teacher_name}</td>
                        <td style={{ padding: 8 }}>{new Date(r.created_at).toLocaleDateString()}</td>
                        <td style={{ padding: 8 }}>{Math.round(r.duration_seconds / 60)} min</td>
                        <td style={{ padding: 8 }}><a href={`https://mock-s3-endpoint.r2.cloudflarestorage.com/mock-bucket/${r.r2_key}`} target="_blank">Download MP4</a></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      )}

      {user.role === 'teacher' && (
        <div>
          <h2>Teacher Portal</h2>
          <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, backgroundColor: "#f9f9f9", marginBottom: 16 }}>
            <h3>Start a Class</h3>
            <p>Your permanent meeting ID is associated with your account.</p>
            <button onClick={() => navigate("/class/my-room")} style={{ padding: "8px 16px", cursor: "pointer", backgroundColor: "#007bff", color: "white", border: "none" }}>Start Class</button>
          </div>
          
          <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, backgroundColor: "#f0fdf4" }}>
            <h3>Past Classes & Feedback</h3>
            {teacherHistory.length === 0 ? <p>No past classes with AI feedback yet.</p> : (
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {teacherHistory.map(h => (
                  <div key={h.id} style={{ border: "1px solid #ccc", padding: 12, borderRadius: 8, backgroundColor: "white" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
                      <strong>{new Date(h.created_at).toLocaleString()}</strong>
                      <span style={{ 
                        padding: "2px 8px", 
                        borderRadius: 12, 
                        fontWeight: "bold", 
                        backgroundColor: h.ai_grade?.startsWith('A') ? '#4caf50' : '#ff9800',
                        color: 'white'
                      }}>
                        Grade: {h.ai_grade || 'Pending'}
                      </span>
                    </div>
                    <p style={{ margin: 0, color: "#555" }}>{h.ai_feedback || 'AI analysis is currently processing this recording...'}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {user.role === 'student' && (
        <div>
          <h2>Student Portal</h2>
          <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 8, backgroundColor: "#f9f9f9" }}>
            <h3>Join a Class</h3>
            <form onSubmit={(e) => {
              e.preventDefault();
              const classId = (e.target as any).classId.value;
              if (classId) navigate(`/class/${classId}`);
            }} style={{ display: "flex", gap: 8 }}>
              <input name="classId" placeholder="Class ID (e.g. my-room)" required style={{ padding: 8, flex: 1 }} />
              <button type="submit" style={{ padding: "8px 16px", cursor: "pointer", backgroundColor: "#007bff", color: "white", border: "none" }}>Join</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
