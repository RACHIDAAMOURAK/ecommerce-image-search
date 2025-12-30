import React from 'react';
import './ProductCard.css';

function ProductCard({ product }) {
  // URL de l'image depuis le backend
  const imageUrl = `http://localhost:5000${product.image_url}`;
  
  return (
    <div className="product-card">
      <div className="product-image-container">
        <img 
          src={imageUrl} 
          alt={product.name}
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/300x300?text=Image+Not+Found';
          }}
        />
        {product.similarity && (
          <div className="similarity-badge">
            {(product.similarity * 100).toFixed(0)}% similaire
          </div>
        )}
      </div>
      
      <div className="product-info">
        <div className="product-category">
          <span className="category-icon">🏷️</span>
          {product.category}
        </div>
        
        <h3 className="product-name">{product.name}</h3>
        
        <p className="product-price">{product.price}</p>
        
        {product.in_stock ? (
          <span className="stock-badge in-stock">En stock</span>
        ) : (
          <span className="stock-badge out-of-stock">Rupture</span>
        )}
      </div>
    </div>
  );
}

export default ProductCard;