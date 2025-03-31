# Detector de Rostos em Imagens
> Projeto desenvolvido para a disciplina de Processamento de Imagens - 2024

Este projeto foi desenvolvido como parte das atividades acadêmicas da disciplina de Processamento de Imagens. O objetivo é criar uma aplicação que detecta rostos em imagens utilizando técnicas de processamento de imagem e visão computacional.

## Funcionalidades

- Interface gráfica intuitiva para seleção de imagens
- Detecção de rostos em imagens
- Processamento de imagens com:
  - Conversão para tons de cinza
  - Suavização
  - Binarização
  - Detecção de bordas
  - Detecção de rostos
- Visualização em tempo real do processamento
- Organização automática das imagens em pastas (com/sem rosto)
- Preview das imagens processadas

## Requisitos

Para executar este projeto, você precisará ter instalado:

- Python 3.x
- OpenCV (cv2)
- NumPy
- Mahotas
- Matplotlib
- Pillow (PIL)
- Tkinter

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/HigorG26/face-recognize.git
cd face-recognize
```

2. Instale as dependências necessárias:
```bash
pip install opencv-python numpy mahotas matplotlib pillow
```

## Como Executar

1. Certifique-se de que todas as dependências estão instaladas
2. Execute o arquivo principal:
```bash
python run.py
```

3. Na interface gráfica que abrir:
   - Clique em "Selecionar Imagens" para escolher as imagens a serem processadas
   - Selecione uma imagem na lista para ver o preview do processamento
   - Clique em "Processar Imagens" para iniciar o processamento em lote

## Estrutura do Projeto

- `run.py`: Arquivo principal que inicializa a aplicação
- `frame.py`: Contém a interface gráfica (GUI)
- `service.py`: Contém a lógica de processamento de imagens

## Organização das Imagens

O programa automaticamente organiza as imagens processadas em duas pastas:
- `imagens_com_rosto/`: Imagens onde foram detectados rostos
- `imagens_sem_rosto/`: Imagens onde não foram detectados rostos

## Observações

- Este é um projeto acadêmico desenvolvido para fins educacionais
- A detecção de rostos utiliza o classificador Haar Cascade do OpenCV
- O processamento de imagens inclui várias etapas para melhorar a detecção
- A interface gráfica foi desenvolvida usando Tkinter para facilitar a interação

## Data de Desenvolvimento

Este projeto foi desenvolvido em março de 2025 como parte das atividades da disciplina de Processamento de Imagens.

## Autor

Higor ?