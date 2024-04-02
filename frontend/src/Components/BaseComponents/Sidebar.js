import React from 'react';
import './Sidebar.css';
import { Link, useNavigate } from 'react-router-dom';

import { useCookies } from 'react-cookie';

const Sidebar = () => {

    const [token, , removeToken] = useCookies(['myToken']);
    const [role, , removeRole] = useCookies(['role']);

    const navigate = useNavigate();



    const logoutSubmitted = () => {
        removeToken('myToken');
        removeRole('role');
        navigate('/');
      };




    return (
        <aside className="sidebar">
            <nav>
                <ul>
                <hr />
                <hr />
                    <li>
                        <Link to="/">
                            <span className="icon">
                                <i className="fas fa-home"></i>
                            </span>
                            || &nbsp; Home
                        
                        </Link>
                    </li>
                    <hr />
                    {role.role === 'admin' && (
                    <li>
                        <Link to="/create-product">
                            <span className="icon">
                                <i className="fas fa-plus"></i>
                            </span>
                            || &nbsp; Create
                           
                        </Link>
                    </li>
                    )}
                    <hr />
                    <li>
                        <Link to="/products">
                            <span className="icon">
                                <i className="fas fa-shopping-cart"></i>
                            </span>
                            || &nbsp; Products
                            
                        </Link>
                    </li>
                    <hr />
                    <li>
                        <Link to="/about">
                            <span className="icon">
                                <i className="fas fa-info-circle"></i>
                            </span>
                            || &nbsp; About
                          
                        </Link>
                    </li>
                    <hr />
                    <li>
                        <Link to="/contact">
                            <span className="icon">
                                <i className="fas fa-envelope"></i>
                            </span>
                            || &nbsp; Contact
                          
                        </Link>
                    </li>
                    <hr />
                    <hr />
                    
                    {token.myToken ? (
                        <div className="auth_btn">
                        <hr />
                        <hr />
                        <hr />
                        <li>
                            <span className="icon">
                                <i className="fas fa-sign-out-alt"></i>
                            </span>
                            <Link onClick={logoutSubmitted}>Log Out</Link>
                        </li>
                            <hr />
                            <hr />
                            <hr />
                        </div>
                    ) : (
                        <div className="auth_btn">
                            <hr />
                            <hr />
                            <hr />
                            <li>
                                <Link to="/login">
                                    <span className="icon">
                                        <i className="fas fa-user"></i>
                                    </span>
                                    Log In
                                </Link>
                            </li>
                            <hr />
                            <hr />
                            <hr />
                        </div>
                    )}
                </ul>
            </nav>
        </aside>
    );
}

export default Sidebar;
