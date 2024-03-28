import React, { useState } from 'react';
import './CreateProduct.css';
import Header from '../BaseComponents/Header';
import Sidebar from '../BaseComponents/Sidebar';
import gif_img from '../../assets/images/ecom_gif.gif';
import { useNavigate } from 'react-router-dom';

const CreateProduct = ({ onCreate }) => {


    let navigate = useNavigate();

    const [name, setName] = useState("")
    const [description, setDescription] = useState("")
    const [price, setPrice] = useState("")
    const [imageUrl, setImageUrl] = useState("")
    const [error, setError] = useState({});
    


  const handleSubmit = async (e) => {
    e.preventDefault();


    // Validation checks
    const errors = {};
    if (!name.trim()) {
        errors.name = "Product name is required";
    }
    if (!price.trim()) {
        errors.price = "Price is required";
    } else if (isNaN(Number(price))) {
        errors.price = "Price must be a number";
    }

    if (Object.keys(errors).length > 0) {
        setError(errors);
        console(error);
        return;
    }


    let formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('image_url', imageUrl);


    let requestOption = {
        method: "POST",
        body: formData,
        redirect: "follow"
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/api/products/', requestOption);
        const responseData = await response.text();
        const jsonResponse = JSON.parse(responseData);

        console.log('success', jsonResponse);
        navigate('/')
    } catch (error) {
        console.log('Error:', error);
    }
    };




  return (
    <>
      <Header />
      <Sidebar />
      <div className="container">
        <div className="image-container">
          <h2>My Ecom Store</h2>
          <img src={gif_img} alt='ecom' height="280px" width="400px" className='imageClass' />
        </div>
        <div className="create-product-container">
          <h2>Create New Product</h2>
          <form onSubmit={handleSubmit} className="create-product-form">
            <input
              type="text"
              name="name"
              onChange={e => setName(e.target.value)} 
              value={name}
              placeholder="Product Name"
              required
            />
            <input
              type="text"
              name="description"
              onChange={e => setDescription(e.target.value)} 
              value={description}
              placeholder="Description"
            />
            <input
              type="number"
              name="price"
              onChange={e => setPrice(e.target.value)} 
              value={price}
              placeholder="Price"
              required
            />
            <input
              type="text"
              name="image_url"
              onChange={e => setImageUrl(e.target.value)} 
              value={imageUrl}
              placeholder="Image URL"
            />
            <button type="submit">Create Product</button>
          </form>
        </div>
      </div>
    </>
  );
};

export default CreateProduct;
