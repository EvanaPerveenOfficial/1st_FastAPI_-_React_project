import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home from './Components/HomePage/Home';
import CreateProduct from './Components/ProductPages/CreateProduct';
import EditProduct from './Components/ProductPages/EditProduct';
import CreateUser from './Components/AuthPages/CreateUser';
import LoginUser from './Components/AuthPages/LoginUser';

import './App.css';


function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="create-product/" element={<CreateProduct/>} />
          <Route path="edit/:productId" element={<EditProduct />} />
          <Route path="sign-up/" element={<CreateUser/>} />
          <Route path="login/" element={<LoginUser/>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
