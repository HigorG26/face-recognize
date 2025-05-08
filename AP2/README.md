# Sistema de Reconhecimento Facial

Este é um sistema de reconhecimento facial que pode identificar pessoas conhecidas através da webcam.

## Requisitos

- Python 3.8 ou superior
- Webcam
- Bibliotecas Python listadas em `requirements.txt`

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Crie uma pasta chamada `imagens_conhecidas` no mesmo diretório do script.

3. Adicione fotos das pessoas que você quer reconhecer na pasta `imagens_conhecidas`. 
   - Use fotos claras e com boa iluminação
   - Nomeie os arquivos com o nome da pessoa (ex: `joao.jpg`, `maria.png`)
   - Cada pessoa deve ter pelo menos uma foto
   - As fotos devem mostrar apenas o rosto da pessoa

## Uso

1. Execute o script:
```bash
python main.py
```

2. O sistema irá:
   - Carregar as imagens de treinamento
   - Iniciar a webcam
   - Mostrar um retângulo vermelho ao redor dos rostos detectados
   - Mostrar o nome da pessoa reconhecida abaixo do retângulo
   - Pessoas não reconhecidas serão marcadas como "Desconhecido"

3. Para sair do programa, pressione a tecla 'q'.

## Observações

- O sistema funciona melhor com boa iluminação
- Evite movimentos bruscos
- Mantenha uma distância adequada da câmera
- Use fotos de treinamento de boa qualidade 