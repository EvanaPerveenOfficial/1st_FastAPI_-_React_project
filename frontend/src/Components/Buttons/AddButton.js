import React from 'react';
import './AddButton.css';

const AddButton = ({ onClick }) => {
  return (
    <button className="add-button" onClick={onClick}>
      +
    </button>
  );
};

export default AddButton;
