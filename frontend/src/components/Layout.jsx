import { Outlet } from 'react-router-dom';
import { CustomLink } from './CustomLink';
import { useContext } from 'react'
import AuthContext from '../context/AuthContext';
import Button from '@material-ui/core/Button';

const Layout = () => {
    let {user, logoutUser} = useContext(AuthContext)
    if (user) {
        return (
        <>
        <header>
            <CustomLink to="/in_search">Chat</CustomLink>
            <CustomLink to="/offline_search">Offline search</CustomLink>
            <CustomLink to="/chats">Chats</CustomLink>
            <CustomLink to="/historical_chats">Historical chats</CustomLink>
            <CustomLink to="/profile">Profile</CustomLink>
            <Button color="#aaaaaa" backgroundColor='#DDDDDD' onClick={logoutUser}>Logout</Button>
        </header>

        <main className="container">
            <Outlet />
        </main>

        <footer className="container">&copy; ReactRouter Tutorials 2021</footer>
        </>
        )
    }
    else return (
        <>
        <header>
            <CustomLink to="/">Chat</CustomLink>
            <CustomLink to="/login">Login</CustomLink>
            <CustomLink to="/registration">Registration</CustomLink>
        </header>

        <main className="container">
            <Outlet />
        </main>

        <footer className="container">&copy; ReactRouter Tutorials 2021</footer>
        </>
    )
}

export {Layout}