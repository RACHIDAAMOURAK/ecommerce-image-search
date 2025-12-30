import os

class Config:
    """Configuration de l'application"""
    
    # Chemins de base
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    PRODUCTS_DIR = os.path.join(DATA_DIR, 'products')
    FEATURES_DIR = os.path.join(DATA_DIR, 'features')
    UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
    
    # Fichiers de données
    METADATA_FILE = os.path.join(DATA_DIR, 'metadata.json')
    FEATURES_DB_FILE = os.path.join(FEATURES_DIR, 'features_db.pkl')
    FEATURES_MATRIX_FILE = os.path.join(FEATURES_DIR, 'features_matrix.npy')
    IMAGE_PATHS_FILE = os.path.join(FEATURES_DIR, 'image_paths.pkl')
    
    # Paramètres du modèle
    IMAGE_SIZE = (224, 224)  # Taille pour ResNet50
    MODEL_NAME = 'ResNet50'
    TOP_K_RESULTS = 10  # Nombre de résultats à retourner
    
    # Configuration Flask
    UPLOAD_FOLDER = UPLOADS_DIR
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    
    # URL de base pour les images
    STATIC_URL = '/static/products'