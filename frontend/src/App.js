import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home from './Components/HomePage/Home';
import CreateProduct from './Components/ProductPages/CreateProduct';
import EditProduct from './Components/ProductPages/EditProduct';

import './App.css';


function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="create-product/" element={<CreateProduct/>} />
          <Route path="edit/:productId" element={<EditProduct />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
