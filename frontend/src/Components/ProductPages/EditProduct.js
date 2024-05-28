import React, { useState, useEffect } from 'react';
import './EditProduct.css';
import Header from '../BaseComponents/Header';
import Sidebar from '../BaseComponents/Sidebar';
import { useNavigate, useParams } from 'react-router-dom';
import { useCookies } from 'react-cookie';

const EditProduct = () => {
    const { productId } = useParams();
    const navigate = useNavigate();
    const [token] = useCookies(['myToken']);

    const [productData, setProductData] = useState({
        name: '',
        description: '',
        price: '',
        image_url: ''
    });

    useEffect(() => {
        fetchProductData(productId);
    }, [productId]);

    const fetchProductData = async (productId) => {
        try {
            const response = await fetch(`http://localhost:8000/api/products/${productId}`, {
                headers: {
                    Authorization: `Bearer ${token.myToken}`
                }
            });
            if (response.ok) {
                const data = await response.json();
                setProductData(data);
            } else {
                console.error('Error fetching product data:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching product data:', error);
        }
    };
    

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setProductData({ ...productData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();


        try {
            const response = await fetch(`http://localhost:8000/api/products/${productId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    // Authorization: `Bearer ${token.myToken}`
                },
                body: JSON.stringify(productData)
            });

            if (response.ok) {
                navigate('/');
            } else {
                console.error('Error updating product:', response.statusText);
            }
        } catch (error) {
            console.error('Error updating product:', error);
        }
    };

    return (
        <>
            <Header />
            <Sidebar />
            <div className="container">
                <div className="edit-product-container">
                    <h2>Edit Product</h2>
                    <form onSubmit={handleSubmit} className="edit-product-form">
                        <input
                            type="text"
                            name="name"
                            value={productData.name}
                            onChange={handleInputChange}
                            placeholder="Product Name"
                            required
                        />
                        <input
                            type="text"
                            name="description"
                            value={productData.description}
                            onChange={handleInputChange}
                            placeholder="Description"
                        />
                        <input
                            type="number"
                            name="price"
                            value={productData.price}
                            onChange={handleInputChange}
                            placeholder="Price"
                            required
                        />
                        <input
                            type="text"
                            name="imageUrl"
                            value={productData.image_url}
                            onChange={handleInputChange}
                            placeholder="Image URL"
                        />
                        <button type="submit">Update Product</button>
                    </form>
                </div>
            </div>
        </>
    );
};

export default EditProduct;
