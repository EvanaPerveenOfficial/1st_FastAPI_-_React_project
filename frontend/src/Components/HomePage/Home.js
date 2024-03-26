import React, { useEffect, useState } from 'react';
import Header from '../BaseComponents/Header';
import Sidebar from '../BaseComponents/Sidebar';
import Cards from '../BaseComponents/Cards';
import AddButton from '../Buttons/AddButton'; // Import AddButton component
import { Link } from 'react-router-dom';

const Home = () => {
    const [cards, setAllCards] = useState([]);
    const [reload, setReload] = useState(false);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/products/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            setAllCards(data); 
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }, [reload]);

    

    const handleDelete = () => {
        setReload(!reload); // Toggle reload to trigger re-render
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
