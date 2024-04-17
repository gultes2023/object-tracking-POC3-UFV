## Problema de Rastreamento de Objetos através de vídeo - Case UFV

#### HUB de Inteligência Artificial - Senai PR

## Participantes
-  [Gustavo Estevam Sena (Residente)](https://github.com/Gultes)
-  [Gustavo Rodrigues Wanke (Residente)](https://github.com/GWanke)

-  [Leonardo Goshi Sanches (Scrum Master)](https://github.com/LeleoSanches)

## Objetivos
- Experimentar modelos de rastreamento de objetos, visando o rastreamento de movimentos de macacos através de imagens áreas realizadas por drones em diferentes ambientes.
- Aplicar os conhecimentos sobre os modelos pesquisados na Sprint 1 em um case envolvendo um problema real.

## Sobre
O trabalho dessa sprint consistiu em experimentar modelos de object tracking levantados na Sprint 1, dentre os quais houve destaque para o sort e deep sort (este segundo aplicado através do yolo BOXMOT). Tal experimentação possibilitou o rastreamento de macacos através das imagens dos vídeos atemporais usados para montagem do dataset na plataforma roboflow, que foi criado pela equipe 1 desse mesmo projeto da UFV, responsável pelo object detection. 

## Arquivos Entregáveios

- sort-implementation: Contém a implementação do modelo matemático sort (sort.ipynb) utilizado para detecção dos macacos através do frame - Primeiro resultado da sprint
- deep-sort-implementation: Contém os notebooks Augmentation.ipynb e feature_extr.ipynb, que foram usados em conjunto com o dataset montado no roboflow
- pela equipe 1 desse mesmo projeto da UFV e o best.pt (O melhor modelo ou versão selecionada para essa tarefa de object detection)  

## Como executar 🏃‍

- Considerando que tem-se acesso ao dataset montado pela equipe 1 e ao best.pt

## Sort (Métodos 1 ou 2)

**1. Execução do Notebook Jupyter localmente:**

- Instale o Jupyter Notebook usando o pip.
- Baixe e extraia o arquivo "sort.ipynb".
- Abra o terminal/prompt de comando.
- Navegue até o diretório onde o arquivo está.
- Inicie o servidor do Jupyter com o comando jupyter notebook.
- No navegador, abra o arquivo "sort.ipynb".
- Execute as células de código conforme necessário.o.
- Salve o notebook quando terminar.
- Encerre o servidor do Jupyter.

**2. Execução do Notebook Jupyter no Google Colab:**

- Acesse o Google Colab no navegador.
- Faça login, se necessário.
- Crie um novo notebook ou faça upload do existente.
- Faça upload do arquivo "sort.ipynb".
- Abra o notebook no Colab.
- Execute as células de código conforme necessário.
- As alterações são salvas automaticamente.
- Encerre a sessão quando terminar.

## Deep Sort (Métodos 1 ou 2)

**Execução do script Python localmente:**

- Certifique-se de ter o Python instalado em seu sistema.
- Abra o terminal/prompt de comando.
- Navegue até o diretório onde o script "track.py" está localizado.
- Execute o comando abaixo:

- python track.py --source ../dataset/macaco.v1i.coco/videos/DJI_20230417130525_0006_T.MP4 --yolo-model tracking/weights/best-yolov8.pt --tracking-method deepocsort --reid-model tracking/weights/reid_resnet50_150.pt --device cpu --project ~/Área\ de\ trabalho/UFV/Sprint\ 2/yolo_tracking/resultados --name video

- Este comando utiliza o script "track.py" para executar o rastreamento de objetos em um vídeo específico.
- Certifique-se de substituir o caminho do vídeo, modelos YOLO e ReID, e o diretório de saída conforme necessário.
- O parâmetro "--device cpu" especifica que o rastreamento será executado na CPU. Se você tiver uma GPU disponível e desejar utilizá-la, substitua "cpu" pelo dispositivo apropriado, como "cuda" para GPUs NVIDIA.
- Após a execução do comando, o resultado do rastreamento será salvo no diretório especificado.

**1. Execução do Notebook Jupyter localmente:**

- Instale o Jupyter Notebook usando o pip, caso ainda não tenha feito isso.
- Baixe e extraia os arquivos "Augmentation.ipynb" e "feature_extr.ipynb".
- Abra o terminal/prompt de comando.
- Navegue até o diretório onde os arquivos estão localizados.
- Inicie o servidor do Jupyter com o comando "jupyter notebook".
- No navegador, abra o arquivo "Augmentation.ipynb".
- Execute as células de código conforme necessário.
- Quando terminar, repita os passos 6 e 7 para o arquivo "feature_extr.ipynb".
- Salve os notebooks quando terminar.
- Encerre o servidor do Jupyter.
- Execução do Notebook Jupyter no Google Colab:

**2. Ou Execução do Notebook Jupyter no Google Colab**

- Faça login, se necessário.
- Crie um novo notebook ou faça upload do existente.
- Faça upload dos arquivos "Augmentation.ipynb" e "feature_extr.ipynb".
- Abra os notebooks no Colab.
- Execute as células de código conforme necessário em cada notebook.
- As alterações são salvas automaticamente.
- Encerre a sessão quando terminar.

````
A execução do Sort.py irá retornar resposta similar ao exemplo da imagem abaixo (Primeiro resultado da sprint 2)

![image](https://github.com/gultes2023/object-tracking-POC3-UFV/assets/131166618/19ecc67d-6734-40fb-926d-8d7f00af8c47)

![image](https://github.com/gultes2023/object-tracking-POC3-UFV/assets/131166618/cad2d4d6-c3a7-4955-81ec-5ed64717288f)

````

````
Já a execução do Deep Sort através do Yolo Tracking vai retornar resposta similar ao exemplo da imagem abaixo (Segundo e melhor resultado da sprint 2)
em um dataset específico que permite a visualização de peixes em movimento irá retornar:

![image](https://github.com/gultes2023/object-tracking-POC3-UFV/assets/131166618/bb6b49e3-53fa-4f60-b652-bbea2438e5f5)

![image](https://github.com/gultes2023/object-tracking-POC3-UFV/assets/131166618/37e26115-2853-4afc-889c-c148ca78d615)

````

Link do vídeo do melhor resulado da sprint 2

(https://www.kaggle.com/datasets/trainingdatapro/fish-tracking-dataset)

