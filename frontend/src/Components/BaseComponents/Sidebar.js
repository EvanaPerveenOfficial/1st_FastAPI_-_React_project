import React from 'react';
import './Sidebar.css';
import { Link, useNavigate } from 'react-router-dom';

import { useCookies } from 'react-cookie';

const Sidebar = () => {

    const [token, , removeToken] = useCookies(['myToken']);
    const navigate = useNavigate();



    const logoutSubmitted = () => {
        removeToken('myToken');
        navigate('/');
      };




    return (
        <aside className="sidebar">
            <nav>
                <ul>
                    <li>
                        <Link to="/">
                            <span className="icon">
                                <i className="fas fa-home"></i>
                            </span>
                            || &nbsp; Home
                            <span className="arrow-icon">
                                <i className="fas fa-chevron-right"></i>
                            </span>
                        </Link>
                    </li>
                    <li>
                        <Link to="/create-product">
                            <span className="icon">
                                <i className="fas fa-plus"></i>
                            </span>
                            || &nbsp; Create
                            <span className="arrow-icon">
                                <i className="fas fa-chevron-right"></i>
                            </span>
                        </Link>
                    </li>
                    <li>
                        <Link to="/products">
                            <span className="icon">
                                <i className="fas fa-shopping-cart"></i>
                            </span>
                            || &nbsp; Products
                            <span className="arrow-icon">
                                <i className="fas fa-chevron-right"></i>
                            </span>
                        </Link>
                    </li>
                    <li>
                        <Link to="/about">
                            <span className="icon">
                                <i className="fas fa-info-circle"></i>
                            </span>
                            || &nbsp; About
                            <span className="arrow-icon">
                                <i className="fas fa-chevron-right"></i>
                            </span>
                        </Link>
                    </li>
                    <li>
                        <Link to="/contact">
                            <span className="icon">
                                <i className="fas fa-envelope"></i>
                            </span>
                            || &nbsp; Contact
                            <span className="arrow-icon">
                                <i className="fas fa-chevron-right"></i>
                            </span>
                        </Link>
                    </li>
                    
                    {token.myToken ? (
                        <div className="auth_btn">
                        <hr />
                        <hr />
                        <hr />
                        <li>
                            <span className="icon">
                                <i className="fas fa-sign-out-alt"></i>
                            </span>
                            <span onClick={logoutSubmitted}>Log Out</span>
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
