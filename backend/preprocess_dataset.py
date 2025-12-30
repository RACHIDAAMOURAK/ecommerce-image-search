import os
import cv2
import numpy as np
from pathlib import Path
from tqdm import tqdm
from config import Config
from preprocessing.image_preprocessing import ImagePreprocessor
import json

def preprocess_all_images():
    """
    Prétraiter toutes les images du dataset et les sauvegarder
    """
    print("=" * 70)
    print("🖼️  PRÉTRAITEMENT DE TOUTES LES IMAGES")
    print("=" * 70)
    
    # Créer le dossier pour les images prétraitées
    preprocessed_dir = os.path.join(Config.DATA_DIR, 'preprocessed')
    os.makedirs(preprocessed_dir, exist_ok=True)
    
    # Charger les métadonnées
    print("\n📂 Chargement des métadonnées...")
    with open(Config.METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print(f"   ✅ {metadata['total_products']} images à prétraiter")
    
    # Initialiser le préprocesseur
    print("\n🔧 Initialisation du préprocesseur...")
    preprocessor = ImagePreprocessor(target_size=Config.IMAGE_SIZE)
    
    # Statistiques
    success_count = 0
    failed_count = 0
    preprocessed_products = []
    
    print("\n⚙️  Prétraitement en cours...\n")
    
    # Prétraiter chaque image
    for product in tqdm(metadata['products'], desc="Prétraitement", unit="image"):
        img_path = product['image_path']
        
        if not os.path.exists(img_path):
            print(f"\n⚠️  Image non trouvée : {img_path}")
            failed_count += 1
            continue
        
        try:
            # Extraire le nom de catégorie et fichier
            category = product['category']
            filename = os.path.basename(img_path)
            
            # Créer le dossier de catégorie dans preprocessed
            category_preprocessed_dir = os.path.join(preprocessed_dir, category)
            os.makedirs(category_preprocessed_dir, exist_ok=True)
            
            # Chemin de sortie
            output_path = os.path.join(category_preprocessed_dir, filename)
            
            # Prétraiter l'image
            img = preprocessor.preprocess_image(img_path, enhance=True)
            
            if img is not None:
                # Reconvertir en uint8 pour sauvegarder
                img_to_save = (img * 255).astype(np.uint8)
                img_to_save = cv2.cvtColor(img_to_save, cv2.COLOR_RGB2BGR)
                
                # Sauvegarder
                cv2.imwrite(output_path, img_to_save)
                
                # Mettre à jour les métadonnées
                product_copy = product.copy()
                product_copy['original_image_path'] = img_path
                product_copy['image_path'] = output_path
                preprocessed_products.append(product_copy)
                
                success_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            print(f"\n❌ Erreur sur {img_path}: {e}")
            failed_count += 1
    
    # Sauvegarder les nouvelles métadonnées
    preprocessed_metadata = {
        'products': preprocessed_products,
        'categories': metadata['categories'],
        'total_products': len(preprocessed_products)
    }
    
    preprocessed_metadata_file = os.path.join(Config.DATA_DIR, 'metadata_preprocessed.json')
    with open(preprocessed_metadata_file, 'w', encoding='utf-8') as f:
        json.dump(preprocessed_metadata, f, indent=4, ensure_ascii=False)
    
    # Récapitulatif
    print("\n" + "=" * 70)
    print("✅ PRÉTRAITEMENT TERMINÉ !")
    print("=" * 70)
    print(f"📊 Statistiques :")
    print(f"   • Images prétraitées avec succès : {success_count}")
    print(f"   • Images en échec : {failed_count}")
    print(f"   • Taux de réussite : {(success_count/metadata['total_products']*100):.1f}%")
    print(f"\n📁 Images prétraitées sauvegardées dans : {preprocessed_dir}")
    print(f"📄 Métadonnées : {preprocessed_metadata_file}")
    print("=" * 70 + "\n")
    
    print("💡 PROCHAINE ÉTAPE : Exécutez build_features_database.py")
    print("   (Le script utilisera automatiquement les images prétraitées)\n")

if __name__ == '__main__':
    preprocess_all_images()