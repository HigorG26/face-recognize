import cv2
import os
from main import FaceRecognizer

def add_new_member():
    # Carregar o modelo existente
    recognizer = FaceRecognizer()
    try:
        recognizer.load_model("modelo_reconhecimento.pkl")
        print("Modelo carregado com sucesso!")
        print(f"Pessoas atualmente reconhecidas: {', '.join(recognizer.get_known_persons())}")
    except Exception as e:
        print(f"Erro ao carregar o modelo: {str(e)}")
        return

    # Diretório com as novas imagens
    new_images_dir = "novas_imagens"
    
    # Verificar se o diretório existe
    if not os.path.exists(new_images_dir):
        print(f"Diretório {new_images_dir} não encontrado!")
        print("Por favor, crie uma pasta 'novas_imagens' e adicione as novas imagens lá.")
        return
    
    # Treinar com as novas imagens
    print("\nAdicionando novos membros...")
    try:
        recognizer.train(new_images_dir, retrain=True)
        recognizer.save_model("modelo_reconhecimento.pkl")
        print("Novos membros adicionados com sucesso!")
        print(f"Pessoas reconhecidas agora: {', '.join(recognizer.get_known_persons())}")
    except Exception as e:
        print(f"Erro ao adicionar novos membros: {str(e)}")

if __name__ == "__main__":
    add_new_member() 