import cv2
import numpy as np
from skimage.feature import corner_harris, corner_peaks, blob_log
from skimage import io, color
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

class FaceRecognizer:
    def __init__(self):
        self.knn = KNeighborsClassifier(n_neighbors=3)
        self.label_encoder = LabelEncoder()
        self.features = []
        self.labels = []
        
    def extract_features(self, image):
        # Converter para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Harris Corner Detection
        harris_corners = corner_harris(gray)
        corner_coords = corner_peaks(harris_corners, min_distance=5)
        
        # Laplacian of Gaussian (LoG) para detecção de blobs
        blobs = blob_log(gray, max_sigma=30, num_sigma=10, threshold=.1)
        
        # Extrair descritores SIFT
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(gray, None)
        
        # Combinar características
        features = []
        if descriptors is not None:
            features.extend(descriptors.mean(axis=0))
        features.extend([len(corner_coords), len(blobs)])
        
        return np.array(features)

    def train(self, data_dir, retrain=False):
        if not retrain and os.path.exists("modelo_reconhecimento.pkl"):
            self.load_model("modelo_reconhecimento.pkl")
            print("Modelo existente carregado. Adicionando novos dados...")
        
        new_features = []
        new_labels = []
        
        for img_file in os.listdir(data_dir):
            if img_file.endswith(('.jpg', '.png', '.jpeg')):
                # Extrair o identificador da pessoa (primeira letra do nome do arquivo)
                person_id = img_file[0]
                
                img_path = os.path.join(data_dir, img_file)
                image = cv2.imread(img_path)
                if image is not None:
                    features = self.extract_features(image)
                    new_features.append(features)
                    new_labels.append(person_id)
        
        if not new_features:
            raise ValueError("Nenhuma imagem válida foi encontrada para treinamento!")
            
        # Combinar com dados existentes se estiver retreinando
        if retrain and self.features:
            self.features.extend(new_features)
            self.labels.extend(new_labels)
        else:
            self.features = new_features
            self.labels = new_labels
            
        # Treinar o classificador
        X = np.array(self.features)
        y = self.label_encoder.fit_transform(self.labels)
        self.knn.fit(X, y)
        
    def predict(self, image):
        features = self.extract_features(image)
        prediction = self.knn.predict([features])[0]
        return self.label_encoder.inverse_transform([prediction])[0]
    
    def save_model(self, model_path):
        with open(model_path, 'wb') as f:
            pickle.dump({
                'knn': self.knn,
                'label_encoder': self.label_encoder,
                'features': self.features,
                'labels': self.labels
            }, f)
    
    def load_model(self, model_path):
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
            self.knn = data['knn']
            self.label_encoder = data['label_encoder']
            self.features = data['features']
            self.labels = data['labels']
            
    def get_known_persons(self):
        return list(set(self.labels))

def main():
    # Criar instância do reconhecedor
    recognizer = FaceRecognizer()
    
    # Diretório com as imagens de treinamento
    data_dir = "imagens"
    
    # Treinar o modelo
    print("Treinando o modelo...")
    try:
        # Primeiro treinamento
        recognizer.train(data_dir)
        # Salvar o modelo treinado
        recognizer.save_model("modelo_reconhecimento.pkl")
        print("Modelo treinado e salvo com sucesso!")
        print(f"Pessoas reconhecidas: {', '.join(recognizer.get_known_persons())}")
    except Exception as e:
        print(f"Erro durante o treinamento: {str(e)}")

if __name__ == "__main__":
    main()
