import { Link, useMatch } from 'react-router-dom';

const CustomLink = ({children, to, ...props}) => {
    const match = useMatch({
        path: to,
        end: to.length === 1,
    });

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

export {CustomLink};