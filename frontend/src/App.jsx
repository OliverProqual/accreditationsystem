import { useState } from 'react';
import Login from './components/Login'
import Dashboard from './components/Dashboard';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  if (!token) {
    return <Login onLogin={setToken} />;
  }

  return <Dashboard />;
}

export default App;

