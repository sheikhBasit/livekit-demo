import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Classroom from './Classroom';
import Dashboard from './Dashboard';
import ManageUsers from './ManageUsers';

function PrivateRoute({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route 
        path="/" 
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } 
      />
      <Route 
        path="/admin/users" 
        element={
          <PrivateRoute>
            <ManageUsers />
          </PrivateRoute>
        } 
      />
      <Route 
        path="/class/:classId" 
        element={
          <PrivateRoute>
            <Classroom />
          </PrivateRoute>
        } 
      />
    </Routes>
  );
}
