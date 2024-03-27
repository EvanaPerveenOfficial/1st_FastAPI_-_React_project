import React from 'react';
import './Cards.css';
import alt_img from'../../assets/images/alt_image.png';
import { Link } from 'react-router-dom';
// import { useNavigate } from 'react-router-dom';




const Cards = ({ cards, onDelete }) => {

    // const navigate = useNavigate();

    const deleteProduct = async (productId) => {
        try {
            const response = await fetch(`http://localhost:8000/api/products/${productId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {

                onDelete();
                console.log("Successfull");

            } else {
                console.error('Failed to delete product:', response.statusText);
            }
        } catch (error) {
            console.error('Error deleting product:', error);
        }
    };


    return (
        <div className="cards">
            {cards.map((product, index) => (
                <div key={index} className="card">
                    <div className="card-image-container">
                        <img src={product.image_url ? `${process.env.PUBLIC_URL}${product.image_url}` : alt_img} alt={product.name} height="250px" width="280px" className='imageClass' />
                        <button className="delete-icon-button" onClick={() => deleteProduct(product.id)}><i className="fas fa-trash-alt"></i></button>
                    </div>
                    <h2>{product.name}</h2>
                    <p>{product.description}</p>
                    <p>Price: ${product.price}</p>
                    <div className="card-buttons">
                        <Link to={`/edit/${product.id}`} className="edit-button">Edit</Link>
                        <button className="add-to-cart-button">Add to cart</button>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default Cards;