import React, { useEffect, useState } from 'react';
import Header from '../BaseComponents/Header';
import Sidebar from '../BaseComponents/Sidebar';
import Cards from '../BaseComponents/Cards';
import AddButton from '../Buttons/AddButton'; 
import { Link } from 'react-router-dom';
import { useCookies } from 'react-cookie';

const Home = () => {
    const [cards, setAllCards] = useState([]);
    const [reload, setReload] = useState(false);
    const [token] = useCookies(['myToken']);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/products/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token.myToken}`,

            }
        })
        .then(response => response.json())
        .then(data => {
            setAllCards(data); 
            console.log("my_token", token.myToken);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, [token,reload]);

    

    const handleDelete = () => {
        setReload(!reload);
    };

    return (
        <>
            <Header />
            <Sidebar />
            <div>
                <Cards cards={cards} onDelete={handleDelete} />
            </div>
            <Link to="/create-product"> {/* Link to CreateProduct page */}
                <AddButton />
            </Link>
        </>
    );
};

export default Home;
