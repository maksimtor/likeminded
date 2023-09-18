import React, { Routes, Route, BrowserRouter as Router } from 'react-router-dom';

import { Layout } from './components/Layout'

import Chatsearch from './pages/Chatsearch';

import Loginpage from './pages/Loginpage';
import Regpage from './pages/Regpage';

import InChatSearch from './pages/InChatSearch';
import Profile from './pages/Profile';

import { AuthProvider } from './context/AuthContext'

import { RequireAnon } from './context/RequireAnon'
import { RequireAuth } from './context/RequireAuth'
import "./App.css";


function App() {
    return (
      <>
        <Router>
          <AuthProvider>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<RequireAnon><Chatsearch /></RequireAnon>} />
                <Route path='in_search' element={<RequireAuth><InChatSearch /></RequireAuth>} />
                <Route path='profile' element={<RequireAuth><Profile /></RequireAuth>} />
                <Route path='login' element={
                  <RequireAnon>
                    <Loginpage />
                  </RequireAnon>
                } />
                <Route path='registration' element={<RequireAnon><Regpage /></RequireAnon>} />
              </Route>
            </Routes>
          </AuthProvider>
        </Router>
      </>
    );
  }

export default App;