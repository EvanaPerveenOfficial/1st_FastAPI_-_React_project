import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home from './Components/HomePage/Home';
import CreateProduct from './Components/ProductPages/CreateProduct';
import EditProduct from './Components/ProductPages/EditProduct';
import CreateUser from './Components/AuthPages/CreateUser';

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
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
