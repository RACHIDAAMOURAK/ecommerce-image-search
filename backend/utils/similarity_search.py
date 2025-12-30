import numpy as np
import pickle

class SimilaritySearch:
    def __init__(self, features_matrix, image_paths, metric='cosine'):
        self.features_matrix = features_matrix
        self.image_paths = image_paths
        self.metric = metric

    def find_similar(self, query_features, top_k=5):
        if self.metric == 'cosine':
            similarities = np.dot(self.features_matrix, query_features) / (
                np.linalg.norm(self.features_matrix, axis=1) * np.linalg.norm(query_features)
            )
            indices = np.argsort(similarities)[::-1][:top_k]
        else:
            distances = np.linalg.norm(self.features_matrix - query_features, axis=1)
            indices = np.argsort(distances)[:top_k]

        return [(self.image_paths[i], similarities[i] if self.metric == 'cosine' else distances[i]) for i in indices]

    def save_data(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_data(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)