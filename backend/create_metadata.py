import os
import json
from pathlib import Path
from config import Config

def create_metadata():
    """
    Créer un fichier JSON avec les informations de tous les produits
    """
    products_dir = Config.PRODUCTS_DIR
    metadata = {
        'products': [],
        'categories': [],
        'total_products': 0
    }
    
    product_id = 1
    
    print(f"📁 Scan du dossier : {products_dir}\n")
    
    # Parcourir tous les dossiers (catégories)
    for category_folder in sorted(os.listdir(products_dir)):
        category_path = os.path.join(products_dir, category_folder)
        
        if os.path.isdir(category_path):
            print(f"📂 Catégorie : {category_folder}")
            
            # Ajouter la catégorie
            if category_folder not in metadata['categories']:
                metadata['categories'].append(category_folder)
            
            category_count = 0
            
            # Parcourir toutes les images dans ce dossier
            for image_file in sorted(os.listdir(category_path)):
                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(category_path, image_file)
                    
                    # Créer l'entrée du produit
                    product = {
                        'id': product_id,
                        'name': f"{category_folder.capitalize()} #{product_id}",
                        'category': category_folder,
                        'image_path': image_path.replace('\\', '/'),
                        'image_url': f"/products/{category_folder}/{image_file}",
                        'price': f"{(20 + (product_id * 7) % 180)}.99 €",
                        'description': f"Beautiful {category_folder} from our collection",
                        'in_stock': True
                    }
                    
                    metadata['products'].append(product)
                    product_id += 1
                    category_count += 1
            
            print(f"   ✅ {category_count} produits trouvés\n")
    
    metadata['total_products'] = len(metadata['products'])
    
    # Créer le dossier si nécessaire
    os.makedirs(os.path.dirname(Config.METADATA_FILE), exist_ok=True)
    
    # Sauvegarder le fichier JSON
    with open(Config.METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print(f"✅ MÉTADONNÉES CRÉÉES AVEC SUCCÈS !")
    print(f"{'='*70}")
    print(f"📊 Statistiques :")
    print(f"   • Produits totaux : {metadata['total_products']}")
    print(f"   • Catégories : {len(metadata['categories'])}")
    print(f"   • Liste des catégories : {', '.join(metadata['categories'])}")
    print(f"\n💾 Fichier sauvegardé : {Config.METADATA_FILE}")
    print(f"{'='*70}\n")
    
    return metadata

if __name__ == '__main__':
    create_metadata()