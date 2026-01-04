import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ImageSearch from './ImageSearch';
import ProductCard from './ProductCard';
import './HomePage.css';

function HomePage() {
  const [randomProducts, setRandomProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRandomProducts();
  }, []);

  const loadRandomProducts = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/products/random?count=20');
      if (response.data.success) {
        setRandomProducts(response.data.products);
      }
    } catch (error) {
      console.error('Error loading products:', error);
      alert('Error while loading products');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="homepage">
      <header className="header">
        <h1>🛍️ E-Commerce Image Search</h1>
        <p className="tagline">Find your favorite products in one click</p>
      </header>

      <ImageSearch />

      <section className="random-products-section">
        <div className="section-header">
          <h2>Discover Our Products</h2>
          <p>A random selection to inspire you</p>
          <button onClick={loadRandomProducts} className="refresh-btn" disabled={loading}>
            🔄 {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>
        
        {loading ? (
          <div className="loading">Loading products...</div>
        ) : (
          <div className="products-grid">
            {randomProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </section>

      <footer className="footer">
        <p>© 2025 E-Commerce Image Search - Data Science Project</p>
      </footer>
    </div>
  );
}

export default HomePage;
