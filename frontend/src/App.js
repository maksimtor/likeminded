import { Routes, Route, Navigate, BrowserRouter as Router, Link } from 'react-router-dom';

import { Layout } from './components/Layout'

import Chatsearch from './pages/Chatsearch';

import Loginpage from './pages/Loginpage';
import Regpage from './pages/Regpage';

import InChatSearch from './pages/InChatSearch';
import OfflineSearch from './pages/OfflineSearch';
import Chats from './pages/Chats';
import HistoricalChats from './pages/HistoricalChats';
import Profile from './pages/Profile';

import { AuthProvider } from './context/AuthContext'

import { RequireAnon } from './context/RequireAnon'
import { RequireAuth } from './context/RequireAuth'
import "./App.css";


function App() {
  if (true){
    return (
      <>
      <Router>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<RequireAnon><Chatsearch /></RequireAnon>} />
              <Route path='in_search' element={<RequireAuth><InChatSearch /></RequireAuth>} />
              <Route path='offline_search' element={<RequireAuth><OfflineSearch /></RequireAuth>} />
              <Route path='chats' element={<RequireAuth><Chats /></RequireAuth>} />
              <Route path='historical_chats' element={<RequireAuth><HistoricalChats /></RequireAuth>} />
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
}

export default App;