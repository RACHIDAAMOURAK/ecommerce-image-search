import React from 'react';
import ProductCard from './ProductCard';

function SearchResults({ results, queryImage, onBackToHome }) {
  return (
    <div className="search-results-page">
      {/* Header */}
      <header className="results-header">
        <button onClick={onBackToHome} className="back-button">
          ← Back
        </button>
        <h1>Search Results</h1>
      </header>

      {/* Query image */}
      <section className="query-section">
        <h2>Your Image</h2>
        <div className="query-image-container">
          <img src={queryImage} alt="Query" className="query-image" />
        </div>
      </section>

      {/* Results */}
      <section className="results-section">
        <h2>Similar Products ({results.length})</h2>
        
        {results.length === 0 ? (
          <div className="no-results">
            <p>No similar products found 😔</p>
            <button onClick={onBackToHome} className="try-again-btn">
              Try another image
            </button>
          </div>
        ) : (
          <div className="products-grid">
            {results.map((product) => (
              <ProductCard 
                key={product.id} 
                product={product} 
                showSimilarity={true}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default SearchResults;
