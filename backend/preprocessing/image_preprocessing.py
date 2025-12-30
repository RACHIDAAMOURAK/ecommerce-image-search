import cv2
import numpy as np
from PIL import Image
import os
from config import Config

class ImagePreprocessor:
    """
    Classe pour le prétraitement des images
    """
    
    def __init__(self, target_size=None):
        """
        Args:
            target_size (tuple): Taille cible (largeur, hauteur)
        """
        self.target_size = target_size or Config.IMAGE_SIZE
    
    def preprocess_image(self, image_path, enhance=False):
        """
        Prétraitement complet d'une image
        
        Args:
            image_path (str): Chemin vers l'image
            enhance (bool): Appliquer des améliorations (contraste, bruit)
            
        Returns:
            numpy.ndarray: Image prétraitée (normalisée entre 0 et 1)
        """
        try:
            # 1. Charger l'image
            img = cv2.imread(image_path)
            
            if img is None:
                print(f"❌ Impossible de charger : {image_path}")
                return None
            
            # 2. Convertir BGR (OpenCV) vers RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # 3. Redimensionner
            img = cv2.resize(img, self.target_size, interpolation=cv2.INTER_AREA)
            
            # 4. Améliorations optionnelles
            if enhance:
                img = self.enhance_image(img)
                img = self.denoise_image(img)
            
            # 5. Normalisation (0-1)
            img = img.astype(np.float32) / 255.0
            
            return img
            
        except Exception as e:
            print(f"❌ Erreur lors du prétraitement de {image_path}: {e}")
            return None
    
    def enhance_image(self, img):
        """
        Améliorer le contraste de l'image avec CLAHE
        
        Args:
            img (numpy.ndarray): Image RGB
            
        Returns:
            numpy.ndarray: Image avec contraste amélioré
        """
        # Convertir en LAB (meilleur pour améliorer le contraste)
        lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Appliquer CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Fusionner et reconvertir en RGB
        lab = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        return enhanced
    
    def denoise_image(self, img):
        """
        Réduire le bruit dans l'image
        
        Args:
            img (numpy.ndarray): Image RGB
            
        Returns:
            numpy.ndarray: Image débruitée
        """
        # Utiliser le filtrage Non-Local Means Denoising
        denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        return denoised
    
    def remove_background(self, img):
        """
        Supprimer le fond de l'image (optionnel - avancé)
        Utilise GrabCut
        
        Args:
            img (numpy.ndarray): Image RGB
            
        Returns:
            numpy.ndarray: Image avec fond supprimé
        """
        # Créer un masque
        mask = np.zeros(img.shape[:2], np.uint8)
        
        # Définir un rectangle contenant l'objet principal
        rect = (10, 10, img.shape[1]-10, img.shape[0]-10)
        
        # Modèles pour GrabCut
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        # Appliquer GrabCut
        cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        
        # Créer le masque final
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # Appliquer le masque
        img_no_bg = img * mask2[:, :, np.newaxis]
        
        return img_no_bg
    
    def check_image_quality(self, image_path):
        """
        Vérifier la qualité d'une image
        
        Args:
            image_path (str): Chemin vers l'image
            
        Returns:
            dict: Statistiques sur l'image
        """
        img = cv2.imread(image_path)
        
        if img is None:
            return None
        
        # Convertir en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Calculer la netteté (variance du Laplacien)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculer la luminosité moyenne
        brightness = np.mean(gray)
        
        # Calculer le contraste
        contrast = np.std(gray)
        
        return {
            'sharpness': sharpness,
            'brightness': brightness,
            'contrast': contrast,
            'size': img.shape
        }

# Test du module
if __name__ == '__main__':
    print("🧪 Test du Image Preprocessor\n")
    
    preprocessor = ImagePreprocessor()
    
    # Tester sur une image
    test_image = 'data/products/bag/bag1.png'
    
    if os.path.exists(test_image):
        print(f"📷 Test sur : {test_image}\n")
        
        # Vérifier la qualité
        quality = preprocessor.check_image_quality(test_image)
        if quality:
            print("📊 Qualité de l'image :")
            print(f"   Netteté : {quality['sharpness']:.2f}")
            print(f"   Luminosité : {quality['brightness']:.2f}")
            print(f"   Contraste : {quality['contrast']:.2f}")
            print(f"   Taille : {quality['size']}\n")
        
        # Prétraiter
        img = preprocessor.preprocess_image(test_image, enhance=True)
        
        if img is not None:
            print(f"✅ Image prétraitée avec succès !")
            print(f"   Shape : {img.shape}")
            print(f"   Min : {img.min():.3f}, Max : {img.max():.3f}")
    else:
        print(f"❌ Image de test non trouvée : {test_image}")