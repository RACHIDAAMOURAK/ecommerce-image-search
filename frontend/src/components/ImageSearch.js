import React, { useState } from 'react';
import axios from 'axios';
import ProductCard from './ProductCard';
import './ImageSearch.css';

function ImageSearch() {
  const [searchText, setSearchText] = useState('');
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchType, setSearchType] = useState(''); // 'text' or 'image'

  // Text search
  const handleTextSearch = async () => {
    if (!searchText.trim()) {
      alert('Please enter a search term');
      return;
    }

    setLoading(true);
    setSearchType('text');

    try {
      const response = await axios.get('/api/search/text', {
        params: { query: searchText }
      });

      if (response.data.success) {
        setResults(response.data.results);
      } else {
        alert('No products found');
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Error during search: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Image selection
  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(file);
      setPreviewUrl(URL.createObjectURL(file));
      // Automatically start the search
      handleImageSearch(file);
    }
  };

  // Image search
  const handleImageSearch = async (file) => {
    if (!file && !selectedImage) {
      alert('Please select an image');
      return;
    }

    const imageToSearch = file || selectedImage;
    setLoading(true);
    setSearchType('image');

    const formData = new FormData();
    formData.append('image', imageToSearch);

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
        alert('Error during search');
      }
    } catch (error) {
      console.error('Search error:', error);
      alert('Error during search: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  // Clear all
  const handleClear = () => {
    setSearchText('');
    setSelectedImage(null);
    setPreviewUrl(null);
    setResults([]);
    setSearchType('');
  };

  // Handle Enter key in search field
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleTextSearch();
    }
  };

  return (
    <div className="image-search-container">
      <div className="search-box">
        <h2>🔍 Search Products</h2>
        <p className="subtitle">Search by name, category, or upload an image</p>
        
        {/* MAIN SEARCH BAR */}
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search product, brand, or category..."
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onKeyPress={handleKeyPress}
            className="search-input"
          />
          
          {/* Text search button */}
          <button 
            onClick={handleTextSearch} 
            disabled={loading}
            className="search-button"
            title="Search by text"
          >
            🔍
          </button>
          
          {/* Image upload button */}
          <label htmlFor="image-upload" className="camera-button" title="Search by image">
            📷
            <input
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              id="image-upload"
              style={{ display: 'none' }}
            />
          </label>
        </div>

        {/* IMAGE PREVIEW IF UPLOADED */}
        {previewUrl && (
          <div className="preview-section">
            <div className="preview-image">
              <img src={previewUrl} alt="Preview" />
              <button onClick={handleClear} className="remove-image">❌</button>
            </div>
          </div>
        )}

        {/* LOADING INDICATOR */}
        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Searching...</p>
          </div>
        )}
      </div>

      {/* RESULTS */}
      {results.length > 0 && (
        <div className="results-section">
          <div className="results-header">
            <h3>
              {searchType === 'text' ? '📝' : '📷'} 
              {' '}Results ({results.length} products)
            </h3>
            <button onClick={handleClear} className="clear-results-btn">
              New search
            </button>
          </div>
          <div className="results-grid">
            {results.map((product, index) => (
              <ProductCard key={index} product={product} showSimilarity={searchType === 'image'} />
            ))}
          </div>
        </div>
      )}

      {/* NO RESULTS */}
      {!loading && results.length === 0 && searchType && (
        <div className="no-results">
          <p>😔 No products found</p>
          <button onClick={handleClear} className="try-again-btn">
            Try another search
          </button>
        </div>
      )}
    </div>
  );
}

export default ImageSearch;