# 🛍️ E-commerce Image Search - Guide Complet

## 📖 Description du Projet

Application web e-commerce permettant de rechercher des produits par image (CBIR - Content-Based Image Retrieval).

### Fonctionnalités
- ✅ Upload d'image et recherche par similarité
- ✅ Affichage de produits aléatoires sur la page d'accueil
- ✅ Prétraitement des images (débruitage, amélioration de contraste)
- ✅ Extraction de features avec ResNet50
- ✅ Recherche par similarité cosine
- ✅ Interface React moderne et responsive

---

## 📁 Structure du Projet

```
ecommerce-image-search/
├── backend/
│   ├── data/
│   │   ├── products/           # ⭐ VOTRE DATASET ICI
│   │   │   ├── bag/
│   │   │   ├── boot/
│   │   │   ├── coat/
│   │   │   └── ...
│   │   ├── features/           # Généré automatiquement
│   │   └── metadata.json       # Généré automatiquement
│   ├── models/
│   │   └── feature_extractor.py
│   ├── preprocessing/
│   │   └── image_preprocessing.py
│   ├── utils/
│   │   └── similarity.py
│   ├── app.py
│   ├── config.py
│   ├── create_metadata.py
│   ├── build_features_database.py
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── App.js
    │   └── App.css
    └── package.json
```

---

## 🚀 INSTALLATION - ÉTAPE PAR ÉTAPE

### ÉTAPE 1: Préparer l'environnement Backend

```bash
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur Mac/Linux:
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

⚠️ **Note**: L'installation de TensorFlow peut prendre plusieurs minutes.

---

### ÉTAPE 2: Organiser votre Dataset

Placez vos images dans `backend/data/products/` selon cette structure:

```
backend/data/products/
├── bag/
│   ├── bag1.png
│   ├── bag2.png
│   └── ...
├── boot/
│   └── ...
├── coat/
│   └── ...
└── tshirt/
    └── ...
```

✅ **Formats supportés**: PNG, JPG, JPEG, WEBP

---

### ÉTAPE 3: Créer le fichier metadata.json

```bash
# Dans backend/ avec l'environnement virtuel activé
python create_metadata.py
```

**Sortie attendue:**
```
============================================================
🏗️  CRÉATION DU FICHIER METADATA.JSON
============================================================
📁 Catégories trouvées: ['bag', 'boot', 'coat', ...]
   • bag: 8 images
   • boot: 12 images
   • coat: 10 images
   ...
✅ Metadata créé avec succès!
   📄 Fichier: data/metadata.json
   📦 Total produits: 150
   🏷️  Catégories: 13
```

---

### ÉTAPE 4: Construire la base de features

**⚠️ IMPORTANT**: Cette étape peut prendre 5-20 minutes selon:
- Le nombre d'images (1-2 secondes par image)
- Votre processeur (CPU)
- Si vous avez un GPU NVIDIA avec CUDA, ce sera beaucoup plus rapide

```bash
# Dans backend/ avec l'environnement virtuel activé
python build_features_database.py
```

**Sortie attendue:**
```
============================================================
🏗️  CONSTRUCTION DE LA BASE DE FEATURES
============================================================

📖 Chargement de metadata.json...
✓ 150 produits chargés

🔧 Initialisation du prétraitement (modèle: ResNet50)...

🤖 Chargement du modèle d'extraction de features...
Downloading data from https://storage.googleapis.com/...
✓ Modèle chargé. Dimension des features: 2048

⚙️  Prétraitement et extraction des features...
Processing: 100%|████████████████| 150/150 [03:45<00:00,  1.50s/it]

✅ Extraction terminée!
   • Images traitées: 150/150
   • Échecs: 0
   • Dimension des features: (150, 2048)

💾 Sauvegarde des features...
   ✓ data/features/features_matrix.npy
   ✓ data/features/image_paths.pkl
   ✓ data/features/features_db.pkl

✅ Base de features construite avec succès!
   📊 Dimensions: (150, 2048)
   🎯 Prêt pour la recherche par similarité!
```

---

### ÉTAPE 5: Lancer le serveur Backend

```bash
# Dans backend/ avec l'environnement virtuel activé
python app.py
```

**Sortie attendue:**
```
🚀 Initialisation de l'application...
📖 Chargement metadata...
   ✓ 150 produits
🔧 Initialisation preprocessor...
🤖 Chargement modèle extraction...
✓ Modèle chargé. Dimension des features: 2048
💾 Chargement features database...
🔍 Initialisation recherche similarité...
✓ Système de recherche initialisé avec 150 images
✅ Application prête!

🌐 Serveur démarré sur http://0.0.0.0:5000
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.x:5000
```

✅ **Le backend est prêt!** Laissez ce terminal ouvert.

---

### ÉTAPE 6: Installer le Frontend

**Ouvrez un NOUVEAU terminal** (laissez le backend tourner):

```bash
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances Node.js
npm install
```

---

### ÉTAPE 7: Lancer le Frontend

```bash
# Dans frontend/
npm start
```

**Le navigateur s'ouvrira automatiquement sur http://localhost:3000**

---

## 🧪 COMMENT TESTER

### Test 1: Vérifier la page d'accueil
1. Ouvrez http://localhost:3000
2. Vous devriez voir:
   - Un header violet avec le titre
   - Une zone de recherche
   - Une grille de 20 produits aléatoires

### Test 2: Recherche par image (méthode 1)
1. Préparez une image de test (ex: un sac, une chaussure)
2. Cliquez sur la zone "Cliquez pour uploader une image"
3. Sélectionnez votre image
4. Attendez quelques secondes
5. ✅ Vous devriez voir les résultats similaires

### Test 3: Recherche avec une image du dataset
1. Allez dans `backend/data/products/bag/`
2. Prenez une image (ex: bag1.png)
3. Uploadez-la dans l'application
4. ✅ Cette même image devrait apparaître en premier résultat (100% match)

### Test 4: Tester l'API directement

**Avec Postman ou cURL:**

```bash
# Test 1: Obtenir des produits aléatoires
curl http://localhost:5000/api/products/random?num=5

# Test 2: Obtenir toutes les catégories
curl http://localhost:5000/api/categories

# Test 3: Recherche par image (avec une image)
curl -X POST -F "image=@/path/to/your/image.jpg" http://localhost:5000/api/search
```

---

## 🔍 VÉRIFICATIONS DE DEBUGGING

### Si le backend ne démarre pas:

```bash
# Vérifier que l'environnement virtuel est activé
# Vous devriez voir (venv) dans votre terminal

# Vérifier que metadata.json existe
ls backend/data/metadata.json

# Vérifier que les features existent
ls backend/data/features/
# Vous devriez voir: features_db.pkl, features_matrix.npy, image_paths.pkl
```

### Si la recherche ne fonctionne pas:

1. **Ouvrir la console du navigateur** (F12)
2. Regarder les erreurs réseau
3. Vérifier que le backend est bien sur http://localhost:5000
4. Tester manuellement: http://localhost:5000/api/products/random

### Si les images ne s'affichent pas:

1. Vérifier que l'URL des images est correcte dans la console
2. Vérifier les permissions des fichiers dans `backend/data/products/`
3. Essayer d'accéder directement: http://localhost:5000/products/bag/bag1.png

---

## 📊 RÉSULTATS ATTENDUS

### Scores de similarité:
- **90-100%**: Image identique ou très similaire
- **70-90%**: Produit similaire (même catégorie, style proche)
- **50-70%**: Ressemblance partielle
- **< 50%**: Peu similaire

### Performance:
- **Temps de recherche**: 1-3 secondes
- **Nombre de résultats**: Top 10 par défaut
- **Qualité**: Dépend de la qualité de votre dataset

---

## 🎨 PERSONNALISATION

### Changer le nombre de résultats:

Dans `frontend/src/App.js`, ligne ~32:
```javascript
formData.append('top_k', '20');  // Au lieu de 10
```

### Changer le modèle d'extraction:

Dans `backend/config.py`:
```python
MODEL_NAME = 'MobileNetV2'  # Plus rapide mais moins précis
# ou
MODEL_NAME = 'ResNet50'  # Plus précis mais plus lent
```

Puis re-construire la base:
```bash
python build_features_database.py
```

### Améliorer la qualité:

Dans `backend/preprocessing/image_preprocessing.py`:
- Ajuster les paramètres de débruitage
- Modifier le contraste
- Ajouter plus d'augmentation de données

---

## 🐛 PROBLÈMES COURANTS

### Erreur: "No module named 'tensorflow'"
```bash
pip install tensorflow==2.15.0
```

### Erreur: "cv2 not found"
```bash
pip install opencv-python
```

### Erreur CORS (Cross-Origin)
- Vérifier que Flask-CORS est installé
- Le backend doit avoir `CORS(app)` dans app.py

### Erreur "Port 5000 already in use"
```bash
# Changer le port dans config.py
FLASK_PORT = 5001
```

### Erreur "npm not found"
- Installer Node.js depuis https://nodejs.org/

---

## 📈 AMÉLIORATIONS POSSIBLES

1. **Ajouter un filtrage par catégorie** dans le frontend
2. **Implémenter la pagination** des résultats
3. **Ajouter un système de panier**
4. **Sauvegarder l'historique de recherche**
5. **Utiliser FAISS** pour une recherche ultra-rapide
6. **Déployer sur le cloud** (Heroku, AWS, Google Cloud)

---

## 📝 RAPPORT DU PROJET

Pour votre mini-projet, incluez:

1. **Introduction**: Objectif du CBIR
2. **Dataset**: Description de vos images (source, catégories, quantité)
3. **Prétraitement**: 
   - Redimensionnement
   - Débruitage (Non-Local Means)
   - Amélioration de contraste (CLAHE)
   - Normalisation
4. **Extraction de features**:
   - Modèle utilisé (ResNet50)
   - Dimension des features (2048)
   - Transfer learning
5. **Recherche par similarité**:
   - Méthode (cosine similarity)
   - Performances (temps, précision)
6. **Interface utilisateur**: Captures d'écran
7. **Résultats**: Exemples de recherches réussies
8. **Conclusion**: Limites et améliorations possibles

---

## 🎓 CONCEPTS TECHNIQUES UTILISÉS

- **Computer Vision**: OpenCV, traitement d'image
- **Deep Learning**: CNN, Transfer Learning, ResNet50
- **Similarity Search**: Cosine similarity, Feature vectors
- **Backend**: Flask, REST API
- **Frontend**: React, Hooks, Axios
- **Data Processing**: NumPy, Pandas

---

## ✅ CHECKLIST FINALE

- [ ] Dataset organisé dans `backend/data/products/`
- [ ] `metadata.json` créé
- [ ] Base de features construite
- [ ] Backend démarré sans erreur
- [ ] Frontend démarré sans erreur
- [ ] Page d'accueil affiche des produits
- [ ] Recherche par image fonctionne
- [ ] Les images s'affichent correctement
- [ ] Scores de similarité cohérents

---

## 📞 AIDE

Si vous rencontrez des problèmes:
1. Vérifiez les logs du backend dans le terminal
2. Vérifiez la console du navigateur (F12)
3. Assurez-vous que tous les fichiers sont aux bons emplacements
4. Relisez les étapes d'installation

**Bon courage pour votre mini-projet! 🚀**