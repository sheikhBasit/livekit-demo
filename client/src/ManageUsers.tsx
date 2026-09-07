import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function ManageUsers() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const [users, setUsers] = useState<any[]>([]);
  const [error, setError] = useState("");
  
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");

  const fetchUsers = async () => {
    try {
      const res = await fetch("http://localhost:8001/api/admin/users", {
        headers: { "Authorization": `Bearer ${token}` }
      });
      const data = await res.json();
      setUsers(data.users || []);
    } catch(e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [token]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch("http://localhost:8001/api/admin/users", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}` 
        },
        body: JSON.stringify({ name, email, password, role })
      });
      if (!res.ok) {
        throw new Error(await res.text());
      }
      setName("");
      setEmail("");
      setPassword("");
      fetchUsers();
    } catch(e: any) {
      setError(e.message || "Failed to create user");
    }
  };

  return (
    <div style={{ fontFamily: "sans-serif", padding: 24, maxWidth: 800, margin: "0 auto" }}>
      <button onClick={() => navigate("/")} style={{ marginBottom: 16 }}>&larr; Back to Dashboard</button>
      <h2>Manage Users</h2>

      <div style={{ padding: 16, border: "1px solid #ccc", borderRadius: 8, marginBottom: 24, backgroundColor: "#f9f9f9" }}>
        <h3>Create New User</h3>
        <form onSubmit={handleCreate} style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} required style={{ padding: 8 }} />
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required style={{ padding: 8 }} />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required style={{ padding: 8 }} />
          <select value={role} onChange={e => setRole(e.target.value)} style={{ padding: 8 }}>
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
            <option value="admin">Admin</option>
          </select>
          <button type="submit" style={{ padding: "8px 16px", cursor: "pointer", backgroundColor: "#007bff", color: "white", border: "none" }}>Create</button>
        </form>
        {error && <p style={{ color: "red", marginTop: 8 }}>{error}</p>}
      </div>

      <h3>Existing Users</h3>
      <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
        <thead>
          <tr style={{ borderBottom: "2px solid #ccc" }}>
            <th style={{ padding: 8 }}>Role</th>
            <th style={{ padding: 8 }}>Name</th>
            <th style={{ padding: 8 }}>Email</th>
            <th style={{ padding: 8 }}>ID</th>
          </tr>
        </thead>
        <tbody>
          {users.map(u => (
            <tr key={u.id} style={{ borderBottom: "1px solid #eee" }}>
              <td style={{ padding: 8, textTransform: "capitalize" }}>{u.role}</td>
              <td style={{ padding: 8 }}>{u.name}</td>
              <td style={{ padding: 8 }}>{u.email}</td>
              <td style={{ padding: 8, fontSize: 12, color: "#666" }}>{u.id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
