import React from 'react';
import './Cards.css';
import alt_img from'../../assets/images/alt_image.png'


const Cards = ({ cards }) => {
    return (
        <div className="cards">
            {cards.map((product, index) => (
                <div key={index} className="card">
                    <img src={product.image_url ? `${process.env.PUBLIC_URL}${product.image_url}` : alt_img} alt={product.name} height="250px" width="280px" className='imageClass' />
                    <h2>{product.name}</h2>
                    <p>{product.description}</p>
                    <p>Price: ${product.price}</p>
                </div>
            ))}
        </div>
    );
}

export default Cards;