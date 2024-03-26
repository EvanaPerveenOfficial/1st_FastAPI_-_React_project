import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home from './Components/HomePage/Home';
import CreateProduct from './Components/ProductPages/CreateProduct';

import './App.css';


function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="create-product/" element={<CreateProduct/>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
