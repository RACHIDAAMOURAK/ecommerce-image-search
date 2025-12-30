import React from 'react';
import ProductCard from './ProductCard';

function SearchResults({ results, queryImage, onBackToHome }) {
  return (
    <div className="search-results-page">
      {/* Header */}
      <header className="results-header">
        <button onClick={onBackToHome} className="back-button">
          ← Retour
        </button>
        <h1>Résultats de recherche</h1>
      </header>

      {/* Image de requête */}
      <section className="query-section">
        <h2>Votre image</h2>
        <div className="query-image-container">
          <img src={queryImage} alt="Query" className="query-image" />
        </div>
      </section>

      {/* Résultats */}
      <section className="results-section">
        <h2>Produits similaires ({results.length})</h2>
        
        {results.length === 0 ? (
          <div className="no-results">
            <p>Aucun produit similaire trouvé 😔</p>
            <button onClick={onBackToHome} className="try-again-btn">
              Essayer une autre image
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