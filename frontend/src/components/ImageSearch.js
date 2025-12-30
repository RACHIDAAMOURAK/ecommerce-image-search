import React, { useState } from 'react';
import axios from 'axios';
import ProductCard from './ProductCard';
import './ImageSearch.css';

function ImageSearch() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResults([]);
    }
  };

  const handleSearch = async () => {
    if (!selectedImage) {
      alert('Veuillez sélectionner une image');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('image', selectedImage);

    try {
      const response = await axios.post(
        '/api/search/image?top_k=12',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      );

      if (response.data.success) {
        setResults(response.data.results);
      } else {
        alert('Erreur lors de la recherche');
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Erreur lors de la recherche: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResults([]);
  };

  return (
    <div className="image-search-container">
      <div className="search-box">
        <h2>🔍 Rechercher par Image</h2>
        <p className="subtitle">Trouvez des produits similaires en téléchargeant une photo</p>
        
        <div className="upload-area">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageSelect}
            id="image-upload"
            style={{ display: 'none' }}
          />
          <label htmlFor="image-upload" className="upload-button">
            📁 Choisir une image
          </label>
          
          <input
            type="file"
            accept="image/*"
            capture="camera"
            onChange={handleImageSelect}
            id="camera-upload"
            style={{ display: 'none' }}
          />
          <label htmlFor="camera-upload" className="camera-button">
            📸 Prendre une photo
          </label>
        </div>

        {previewUrl && (
          <div className="preview-section">
            <div className="preview-image">
              <img src={previewUrl} alt="Preview" />
            </div>
            <div className="preview-actions">
              <button onClick={handleSearch} disabled={loading} className="search-btn">
                {loading ? '⏳ Recherche...' : '🔍 Rechercher'}
              </button>
              <button onClick={handleClear} className="clear-btn">
                ❌ Effacer
              </button>
            </div>
          </div>
        )}
      </div>

      {results.length > 0 && (
        <div className="results-section">
          <h3>Produits similaires ({results.length} résultats)</h3>
          <div className="results-grid">
            {results.map((product, index) => (
              <ProductCard key={index} product={product} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ImageSearch;