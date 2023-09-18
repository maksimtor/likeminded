import React, { Link } from 'react-router-dom';

const CustomLink = ({ children, to, ...props }) => {
    return (
        <Link
            className='nav-links'
            to={to}
            {...props}
        >
            {children}
        </Link>
    )
}

export { CustomLink };