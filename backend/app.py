from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import os
import json
import numpy as np
from werkzeug.utils import secure_filename

from config import Config
from models.feature_extractor import FeatureExtractor
from utils.similarity_search import SimilaritySearch

app = Flask(__name__)
CORS(app)  # Permettre les requêtes depuis le frontend

# Configuration
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# Créer le dossier uploads s'il n'existe pas
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Charger les données au démarrage
print("🚀 Démarrage de l'API...")
print("📂 Chargement des données...")

# Charger les métadonnées
metadata_file = os.path.join(Config.DATA_DIR, 'metadata_preprocessed.json')
if not os.path.exists(metadata_file):
    metadata_file = Config.METADATA_FILE

with open(metadata_file, 'r', encoding='utf-8') as f:
    products_metadata = json.load(f)

print(f"   ✅ {products_metadata['total_products']} produits chargés")

# Charger les features
with open(Config.FEATURES_MATRIX_FILE.replace('.npy', '') + '.npy', 'rb') as f:
    features_matrix = np.load(f)

with open(Config.IMAGE_PATHS_FILE, 'rb') as f:
    image_paths = pickle.load(f)

print(f"   ✅ Features chargées : {features_matrix.shape}")

# Initialiser les modules
feature_extractor = FeatureExtractor(Config.MODEL_NAME)
similarity_search = SimilaritySearch(features_matrix, image_paths, metric='cosine')

print("✅ API prête !\n")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return jsonify({
        'message': 'E-commerce Image Search API',
        'version': '1.0',
        'endpoints': {
            'random_products': '/api/products/random',
            'search_by_image': '/api/search/image',
            'all_products': '/api/products/all'
        }
    })

@app.route('/api/products/random', methods=['GET'])
def get_random_products():
    """
    Retourner des produits aléatoires pour la page d'accueil
    """
    import random
    
    count = int(request.args.get('count', 20))
    count = min(count, len(products_metadata['products']))
    
    random_products = random.sample(products_metadata['products'], count)
    
    # Ajouter l'URL complète des images
    for product in random_products:
        # Convertir le chemin absolu en chemin relatif pour l'URL
        img_path = product['image_path']
        
        # Extraire le chemin relatif (à partir de 'data/')
        if 'data\\products\\' in img_path or 'data/products/' in img_path:
            relative_path = img_path.split('data\\products\\')[-1].replace('\\', '/')
            if 'data/products/' in img_path:
                relative_path = img_path.split('data/products/')[-1]
            product['image_url'] = f'/images/products/{relative_path}'
        elif 'data\\preprocessed\\' in img_path or 'data/preprocessed/' in img_path:
            relative_path = img_path.split('data\\preprocessed\\')[-1].replace('\\', '/')
            if 'data/preprocessed/' in img_path:
                relative_path = img_path.split('data/preprocessed/')[-1]
            product['image_url'] = f'/images/preprocessed/{relative_path}'
    
    return jsonify({
        'success': True,
        'count': len(random_products),
        'products': random_products
    })

@app.route('/api/products/all', methods=['GET'])
def get_all_products():
    """
    Retourner tous les produits
    """
    # Ajouter l'URL complète des images
    all_products = products_metadata['products'].copy()
    
    for product in all_products:
        img_path = product['image_path']
        
        if 'data\\products\\' in img_path or 'data/products/' in img_path:
            relative_path = img_path.split('data\\products\\')[-1].replace('\\', '/')
            if 'data/products/' in img_path:
                relative_path = img_path.split('data/products/')[-1]
            product['image_url'] = f'/images/products/{relative_path}'
        elif 'data\\preprocessed\\' in img_path or 'data/preprocessed/' in img_path:
            relative_path = img_path.split('data\\preprocessed\\')[-1].replace('\\', '/')
            if 'data/preprocessed/' in img_path:
                relative_path = img_path.split('data/preprocessed/')[-1]
            product['image_url'] = f'/images/preprocessed/{relative_path}'
    
    return jsonify({
        'success': True,
        'total': len(all_products),
        'products': all_products
    })

@app.route('/api/search/image', methods=['POST'])
def search_by_image():
    """
    Rechercher des produits similaires à partir d'une image
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Sauvegarder l'image
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extraire les features
            query_features = feature_extractor.extract_features(filepath)
            
            if query_features is None:
                os.remove(filepath)
                return jsonify({'error': 'Failed to extract features'}), 500
            
            # Rechercher les produits similaires
            top_k = int(request.args.get('top_k', 10))
            similar_results = similarity_search.find_similar(query_features, top_k)
            
            # Enrichir avec les métadonnées des produits
            results = []
            for result in similar_results:
                # Trouver le produit correspondant
                matching_product = None
                for product in products_metadata['products']:
                    if product['image_path'] == result[0]:  # Utiliser result[0] pour le chemin de l'image
                        matching_product = product.copy()
                        break
                
                if matching_product:
                    # Ajouter l'URL de l'image
                    img_path = matching_product['image_path']
                    
                    if 'data\\products\\' in img_path or 'data/products/' in img_path:
                        relative_path = img_path.split('data\\products\\')[-1].replace('\\', '/')
                        if 'data/products/' in img_path:
                            relative_path = img_path.split('data/products/')[-1]
                        matching_product['image_url'] = f'/images/products/{relative_path}'
                    elif 'data\\preprocessed\\' in img_path or 'data/preprocessed/' in img_path:
                        relative_path = img_path.split('data\\preprocessed\\')[-1].replace('\\', '/')
                        if 'data/preprocessed/' in img_path:
                            relative_path = img_path.split('data/preprocessed/')[-1]
                        matching_product['image_url'] = f'/images/preprocessed/{relative_path}'
                    
                    # Convertir les valeurs float32 en float
                    matching_product['similarity'] = float(result[1])  # Convertir en float
                    matching_product['rank'] = similar_results.index(result) + 1  # Ajouter le rang
                    results.append(matching_product)
            
            # Nettoyer
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'count': len(results),
                'results': results
            })
        
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

# Servir les images statiques
@app.route('/images/products/<path:filename>')
def serve_product_image(filename):
    """Servir les images du dossier products"""
    return send_from_directory(Config.PRODUCTS_DIR, filename)

@app.route('/images/preprocessed/<path:filename>')
def serve_preprocessed_image(filename):
    """Servir les images du dossier preprocessed"""#ici j'ai fait les images non pretraité 
    preprocessed_dir = os.path.join(Config.DATA_DIR, 'products')
    return send_from_directory(preprocessed_dir, filename)




@app.route('/api/search/text', methods=['GET'])
def search_by_text():
    """
    Rechercher des produits par texte (nom, catégorie, description)
    Query params: query (string)
    """
    query = request.args.get('query', '').strip().lower()
    
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        # Rechercher dans les produits
        results = []
        
        for product in products_metadata['products']:
            # Rechercher dans: nom, catégorie, description
            searchable_text = (
                product.get('name', '').lower() + ' ' +
                product.get('category', '').lower() + ' ' +
                product.get('description', '').lower()
            )
            
            # Si la requête est dans le texte recherchable
            if query in searchable_text:
                product_copy = product.copy()
                
                # Ajouter l'URL de l'image
                img_path = product_copy['image_path']
                
                if 'data\\products\\' in img_path or 'data/products/' in img_path:
                    relative_path = img_path.split('data\\products\\')[-1].replace('\\', '/')
                    if 'data/products/' in img_path:
                        relative_path = img_path.split('data/products/')[-1]
                    product_copy['image_url'] = f'/images/products/{relative_path}'
                elif 'data\\preprocessed\\' in img_path or 'data/preprocessed/' in img_path:
                    relative_path = img_path.split('data\\preprocessed\\')[-1].replace('\\', '/')
                    if 'data/preprocessed/' in img_path:
                        relative_path = img_path.split('data/preprocessed/')[-1]
                    product_copy['image_url'] = f'/images/preprocessed/{relative_path}'
                
                results.append(product_copy)
        
        # Limiter à 20 résultats
        results = results[:20]
        
        return jsonify({
            'success': True,
            'count': len(results),
            'query': query,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
    Retourner toutes les catégories disponibles
    """
    categories = list(set([p['category'] for p in products_metadata['products']]))
    categories.sort()
    
    return jsonify({
        'success': True,
        'count': len(categories),
        'categories': categories
    })






if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Serveur Flask démarré !")
    print("📍 URL : http://localhost:5000")
    print("📁 Images disponibles sur : http://localhost:5000/images/products/")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)