import { Outlet } from 'react-router-dom';
import { CustomLink } from './CustomLink';
import { useContext, useState, useEffect  } from 'react'
import AuthContext from '../context/AuthContext';
import { Button as CustomButton } from './Button';

const Layout = () => {
      const [click, setClick] = useState(false);
    const [button, setButton] = useState(true);

    const handleClick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false);

    const showButton = () => {
        if (window.innerWidth <= 960) {
          setButton(false);
        } else {
          setButton(true);
        }
    };

    useEffect(() => {
        showButton();
    }, []);

    window.addEventListener('resize', showButton);
    let {user, logoutUser} = useContext(AuthContext)
    if (user) {
        return (
        <>
        <header>
            <nav className='navbar'>
            <div className='navbar-container'>
                <CustomLink to='/' className='navbar-logo' onClick={closeMobileMenu}>
                    TRVL
                    <i class='fab fa-typo3' />
                </CustomLink>
              <div className='menu-icon' onClick={handleClick}>
                <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
              </div>
              <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                <li className='nav-item'><CustomLink to="/in_search" onClick={closeMobileMenu}>Chat</CustomLink></li>
               <li className='nav-item'> <CustomLink to="/profile" onClick={closeMobileMenu}>Profile</CustomLink></li>
               {button && <li className='nav-item'><CustomButton buttonStyle='btn--outline' onClick={logoutUser}>Logout</CustomButton></li>}
            </ul>
            </div>
            </nav>
        </header>

        <main className="container">
            <Outlet />
        </main>

        <footer>&copy; ReactRouter Tutorials 2021</footer>
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