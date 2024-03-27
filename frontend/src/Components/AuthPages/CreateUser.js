import React, { useState } from 'react';
import './CreateUser.css';
import { Link, useNavigate } from 'react-router-dom'; 

import gif_img from '../../assets/images/hi_there.gif';

const CreateUser = () => {

    let navigate = useNavigate();

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        const errors = {};

        if (!email.trim()) {
            errors.email = "Email Address is required";
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            errors.email = "Invalid email format";
        }

        if (!password.trim()) {
            errors.password = "Password is required";
        } else if (password.trim().length < 6) {
            errors.password = "Password must be at least 6 characters long";
        }
 
        if (Object.keys(errors).length > 0) {
            console.log(errors);
            return;
        }



        let formData = new FormData();
        formData.append('email', email);
        formData.append('password', password)

        let requestOption = {
            method: 'POST',
            body: formData,
            redirect: 'follow'
        }
        

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/create-user/', requestOption);
            const responseData = await response.text();
            const jsonResponse = JSON.parse(responseData);
            console.log('success', jsonResponse);
            navigate('/');
        } catch (error) {
            console.log('Error: ', error);
        }

    
    };

  return (
    <div className="create-user-container">
        <img src={gif_img} alt='ecom' height="280px" width="450px" className='imageClass' />
      <h2>SignUp Here</h2>
      <form onSubmit={handleSubmit} className="create-user-form">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Create User</button>
      </form>
      <p>
        Already have an account ? {" "}
        <Link to="/signin"> Sign in here</Link> {/* Link to sign-in page */}
      </p>
    </div>
  );
};

export default CreateUser;
