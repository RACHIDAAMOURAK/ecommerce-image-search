import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from config import Config

class FeatureExtractor:
    """
    Extracteur de features utilisant ResNet50 pré-entraîné sur ImageNet
    """
    
    def __init__(self, model_name='ResNet50'):
        """
        Initialiser le modèle pré-entraîné
        
        Args:
            model_name (str): Nom du modèle à utiliser
        """
        print(f"🔄 Chargement du modèle {model_name}...")
        
        # Charger ResNet50 sans la couche de classification (include_top=False)
        # pooling='avg' pour obtenir un vecteur de features de taille fixe
        self.model = ResNet50(
            weights='imagenet',      # Poids pré-entraînés
            include_top=False,       # Sans couche de classification
            pooling='avg',           # Global Average Pooling
            input_shape=(224, 224, 3)
        )
        
        # Le modèle ne sera pas entraîné
        self.model.trainable = False
        
        print(f"✅ Modèle {model_name} chargé avec succès!")
        print(f"   📊 Dimension du vecteur de features : {self.model.output_shape[1]}")
    
    def extract_features(self, img_path):
        """
        Extraire les features d'une seule image
        
        Args:
            img_path (str): Chemin vers l'image
            
        Returns:
            numpy.ndarray: Vecteur de features normalisé (2048 dimensions)
        """
        try:
            # 1. Charger l'image et la redimensionner
            img = image.load_img(img_path, target_size=Config.IMAGE_SIZE)
            
            # 2. Convertir en array numpy
            img_array = image.img_to_array(img)
            
            # 3. Ajouter une dimension batch (le modèle attend (batch, height, width, channels))
            img_array = np.expand_dims(img_array, axis=0)
            
            # 4. Prétraiter selon ResNet50 (normalisation spécifique)
            img_array = preprocess_input(img_array)
            
            # 5. Extraire les features
            features = self.model.predict(img_array, verbose=0)
            
            # 6. Aplatir le vecteur (de (1, 2048) vers (2048,))
            features = features.flatten()
            
            # 7. Normaliser le vecteur (norme L2)
            # Cela permet de comparer les similarités avec le cosine similarity
            norm = np.linalg.norm(features)
            if norm != 0:
                features = features / norm
            
            return features
            
        except Exception as e:
            print(f"❌ Erreur lors de l'extraction de {img_path}: {e}")
            return None
    
    def extract_features_batch(self, img_paths, batch_size=32):
        """
        Extraire les features pour un lot d'images (plus rapide)
        
        Args:
            img_paths (list): Liste des chemins d'images
            batch_size (int): Taille du lot
            
        Returns:
            numpy.ndarray: Matrice de features (n_images, 2048)
        """
        all_features = []
        
        for i in range(0, len(img_paths), batch_size):
            batch_paths = img_paths[i:i+batch_size]
            batch_images = []
            
            # Charger et prétraiter le lot d'images
            for img_path in batch_paths:
                try:
                    img = image.load_img(img_path, target_size=Config.IMAGE_SIZE)
                    img_array = image.img_to_array(img)
                    batch_images.append(img_array)
                except Exception as e:
                    print(f"⚠️  Erreur sur {img_path}: {e}")
                    continue
            
            if len(batch_images) > 0:
                # Convertir en array et prétraiter
                batch_array = np.array(batch_images)
                batch_array = preprocess_input(batch_array)
                
                # Extraire les features
                features = self.model.predict(batch_array, verbose=0)
                
                # Normaliser
                for j in range(len(features)):
                    feature = features[j].flatten()
                    norm = np.linalg.norm(feature)
                    if norm != 0:
                        feature = feature / norm
                    all_features.append(feature)
        
        return np.array(all_features)

# Test du module
if __name__ == '__main__':
    print("🧪 Test du Feature Extractor\n")
    
    # Initialiser l'extracteur
    extractor = FeatureExtractor()
    
    # Tester sur une image
    test_image = 'data/products/bag/bag1.png'
    
    if os.path.exists(test_image):
        print(f"\n📷 Test sur : {test_image}")
        features = extractor.extract_features(test_image)
        
        if features is not None:
            print(f"✅ Features extraites avec succès !")
            print(f"   📊 Shape : {features.shape}")
            print(f"   📏 Norme : {np.linalg.norm(features):.6f}")
            print(f"   📈 Min : {features.min():.6f}, Max : {features.max():.6f}")
    else:
        print(f"❌ Image de test non trouvée : {test_image}")
        print("⚠️  Assurez-vous d'avoir copié votre dataset dans data/products/")