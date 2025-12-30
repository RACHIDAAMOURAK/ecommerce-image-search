import pickle
import json
import numpy as np
from pathlib import Path
from tqdm import tqdm
import os

from config import Config
from models.feature_extractor import FeatureExtractor
# Mise à jour de l'importation pour éviter les boucles
from utils.similarity_search import SimilaritySearch

def build_feature_database():
    """
    Construire la base de features pour TOUS les produits
    Utilise automatiquement les images prétraitées si disponibles
    """
    print("=" * 70)
    print("🚀 CONSTRUCTION DE LA BASE DE FEATURES")
    print("=" * 70)
    
    # 1. Vérifier si les images prétraitées existent
    preprocessed_metadata_file = os.path.join(Config.DATA_DIR, 'metadata_preprocessed.json')
    
    print("\n📂 Chargement des métadonnées...")
    
    if os.path.exists(preprocessed_metadata_file):
        # Utiliser les images PRÉTRAITÉES
        print("   🔍 Images prétraitées détectées !")
        with open(preprocessed_metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print("   ✅ Utilisation des images PRÉTRAITÉES")
        print(f"      Dossier : data/preprocessed/")
    else:
        # Utiliser les images ORIGINALES
        print("   ⚠️  Aucune image prétraitée trouvée")
        print("   💡 Exécutez d'abord : python preprocess_dataset.py")
        with open(Config.METADATA_FILE, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print("   ℹ️  Utilisation des images ORIGINALES")
        print(f"      Dossier : data/products/")
    
    print(f"\n   📊 {metadata['total_products']} produits à traiter")
    
    # 2. Initialiser l'extracteur de features
    print("\n🤖 Initialisation du modèle ResNet50...")
    extractor = FeatureExtractor(Config.MODEL_NAME)
    
    # 3. Extraire les features de toutes les images
    print("\n⚙️  Extraction des features en cours...")
    print("   (Cela peut prendre 5-15 minutes selon votre machine)\n")
    
    features_dict = {}  # {image_path: features}
    features_list = []
    image_paths = []
    valid_products = []
    
    # Barre de progression
    for product in tqdm(metadata['products'], desc="Extraction", unit="image"):
        img_path = product['image_path']
        
        # Vérifier que l'image existe
        if not os.path.exists(img_path):
            print(f"\n⚠️  Image non trouvée : {img_path}")
            continue
        
        # Extraire les features
        features = extractor.extract_features(img_path)
        
        if features is not None:
            features_dict[img_path] = features
            features_list.append(features)
            image_paths.append(img_path)
            valid_products.append(product)
        else:
            print(f"\n❌ Échec extraction : {img_path}")
    
    # 4. Convertir en matrice numpy
    print(f"\n\n📊 Conversion en matrice numpy...")
    features_matrix = np.array(features_list).astype('float32')
    
    print(f"   ✅ Matrice créée : {features_matrix.shape}")
    print(f"      • Nombre d'images : {features_matrix.shape[0]}")
    print(f"      • Dimension des features : {features_matrix.shape[1]}")
    
    # 5. Créer le dossier features s'il n'existe pas
    os.makedirs(Config.FEATURES_DIR, exist_ok=True)
    
    # 6. Sauvegarder les données
    print(f"\n💾 Sauvegarde des données...")
    
    # Sauvegarder le dictionnaire
    with open(Config.FEATURES_DB_FILE, 'wb') as f:
        pickle.dump(features_dict, f)
    print(f"   ✅ Dictionnaire sauvegardé : {Config.FEATURES_DB_FILE}")
    
    # Sauvegarder la matrice
    np.save(Config.FEATURES_MATRIX_FILE, features_matrix)
    print(f"   ✅ Matrice sauvegardée : {Config.FEATURES_MATRIX_FILE}")
    
    # Sauvegarder les chemins d'images
    with open(Config.IMAGE_PATHS_FILE, 'wb') as f:
        pickle.dump(image_paths, f)
    print(f"   ✅ Chemins sauvegardés : {Config.IMAGE_PATHS_FILE}")
    
    # Sauvegarder les produits valides
    valid_metadata = {
        'products': valid_products,
        'categories': metadata['categories'],
        'total_products': len(valid_products)
    }
    
    valid_metadata_file = Config.METADATA_FILE.replace('.json', '_valid.json')
    with open(valid_metadata_file, 'w', encoding='utf-8') as f:
        json.dump(valid_metadata, f, indent=4, ensure_ascii=False)
    print(f"   ✅ Métadonnées valides : {valid_metadata_file}")
    
    # 7. Initialiser le système de recherche
    print(f"\n🔨 Initialisation du système de recherche...")
    print(f"   Métrique : Cosine Similarity")
    
    search_engine = SimilaritySearch(
        features_matrix=features_matrix,
        image_paths=image_paths,
        metric='cosine'
    )
    
    # Sauvegarder l'objet de recherche
    search_data_file = os.path.join(Config.FEATURES_DIR, 'search_engine.pkl')
    search_engine.save_data(search_data_file)
    
    # 8. Récapitulatif
    print("\n" + "=" * 70)
    print("✅ BASE DE FEATURES CRÉÉE AVEC SUCCÈS !")
    print("=" * 70)
    print(f"📊 Statistiques finales :")
    print(f"   • Images traitées : {len(features_list)} / {metadata['total_products']}")
    print(f"   • Images prétraitées : {'Oui' if os.path.exists(preprocessed_metadata_file) else 'Non'}")
    print(f"   • Dimension des features : {features_matrix.shape[1]}")
    print(f"   • Taille totale : {features_matrix.nbytes / (1024*1024):.2f} MB")
    print(f"   • Métrique de similarité : Cosine Similarity & Euclidean Distance")
    print(f"\n📁 Fichiers créés dans : {Config.FEATURES_DIR}")
    print(f"   • features_db.pkl")
    print(f"   • features_matrix.npy")
    print(f"   • image_paths.pkl")
    print(f"   • search_engine.pkl")
    print("=" * 70 + "\n")
    
    return features_matrix, image_paths

if __name__ == '__main__':
    build_feature_database()