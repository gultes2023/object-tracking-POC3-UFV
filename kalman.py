import random
import xml.etree.ElementTree as ET
from filterpy.kalman import KalmanFilter
import numpy as np
import cv2

def parse_xml(xml_file):
    """
    Analisa um arquivo XML de anotações e extrai informações de imagens e anotações.

    :param xml_file: caminho para o arquivo XML a ser analisado
    :return: uma lista de dicionários contendo informações sobre cada imagem e suas anotações
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = []
    for image in root.findall('image'):
        image_info = {
            'id': image.get('id'),
            'file': image.get('name'),
            'annotations': [{
                'label': box.get('label'),
                'occluded': box.get('occluded'),
                'coordinates': {
                    'xtl': float(box.get('xtl')),
                    'ytl': float(box.get('ytl')),
                    'xbr': float(box.get('xbr')),
                    'ybr': float(box.get('ybr'))
                }
            } for box in image.findall('box')]
        }
        data.append(image_info)
    return data

def split_data(data, test_ratio):
    """
    Divide os dados em conjuntos de treinamento e teste com base em uma proporção especificada.

    :param data: lista de dados a serem divididos
    :param test_ratio: proporção dos dados a serem reservados para o conjunto de teste
    :return: duas listas de dados, uma para treinamento e outra para teste
    """
    image_ids = [item['id'] for item in data]
    random.shuffle(image_ids)
    num_test = int(len(image_ids) * test_ratio)
    test_ids = image_ids[:num_test]
    train_ids = image_ids[num_test:]
    train_data = [item for item in data if item['id'] in train_ids]
    test_data = [item for item in data if item['id'] in test_ids]
    return train_data, test_data

def initialize_kalman_filter(x_center, y_center, fish_id):
    """
    Inicializa um filtro de Kalman para rastrear um objeto.

    :param x_center: posição inicial x do centro do objeto
    :param y_center: posição inicial y do centro do objeto
    :param fish_id: identificador do objeto a ser rastreado
    :return: uma instância configurada do filtro de Kalman
    """
    kf = KalmanFilter(dim_x=4, dim_z=2)
    dt = 0.1  # Intervalo de tempo para as previsões do modelo de movimento
    # Matrizes de estado e observação do modelo
    kf.F = np.array([[1, 0, dt, 0],
                     [0, 1, 0, dt],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]]) * 2
    kf.H = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0]]) * 1.01
    # Matrizes de incerteza da medição e do processo
    kf.R = np.eye(2) * 2  # Incerteza da medição
    kf.Q = np.eye(4) * 2  # Incerteza do processo
    kf.P *= 500  # Incerteza inicial estimada do estado
    kf.P[2:, 2:] *= 1000  # Maior incerteza na estimativa inicial da velocidade
    kf.x = np.array([x_center, y_center, 0, 0])  # Estado inicial
    return kf

def process_annotations(training_data):
    """
    Processa anotações para inicializar filtros de Kalman para cada objeto rastreado.

    :param training_data: dados contendo anotações para inicialização
    :return: um dicionário de filtros de Kalman, com chaves únicas para cada objeto
    """
    kalman_filters = {}
    for data_item in training_data:
        for i, annotation in enumerate(data_item['annotations']):
            fish_id = f"{annotation['label']}_{data_item['id']}_{i}"
            x_center = (annotation['coordinates']['xtl'] + annotation['coordinates']['xbr']) / 2
            y_center = (annotation['coordinates']['ytl'] + annotation['coordinates']['ybr']) / 2
            current_measurement = np.array([[x_center], [y_center]])
            if fish_id not in kalman_filters:
                kalman_filters[fish_id] = initialize_kalman_filter(x_center, y_center, fish_id)
            kf = kalman_filters[fish_id]
            kf.predict()
            kf.update(current_measurement)
    return kalman_filters

def draw_box(image, coordinates, color, text):
    """
    Desenha uma caixa e um texto de anotação sobre uma imagem.

    :param image: a imagem onde desenhar
    :param coordinates: coordenadas da caixa (x1, y1, x2, y2)
    :param color: cor da caixa
    :param text: texto para rotular a caixa
    """
    x1, y1, x2, y2 = coordinates
    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
    cv2.putText(image, text, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

def process_images(training_data, kalman_filters):
    """
    Processa imagens para rastreamento de objetos e desenha caixas de anotações reais e estimadas.

    :param training_data: dados de treinamento contendo anotações e caminhos de arquivos de imagem
    :param kalman_filters: dicionário de filtros de Kalman para rastreamento de objetos
    """
    for data_item in training_data:
        image_path = "archive/" + data_item['file']
        image = cv2.imread(image_path)
    
        if image is None:
            print(f"Não foi possível carregar a imagem: {image_path}")
            continue

        for i, annotation in enumerate(data_item['annotations']):
            fish_id = f"{annotation['label']}_{data_item['id']}_{i}"
            if fish_id in kalman_filters:
                kf = kalman_filters[fish_id]
                xtl_real, ytl_real, xbr_real, ybr_real = [annotation['coordinates'][coord] for coord in ['xtl', 'ytl', 'xbr', 'ybr']]
                draw_box(image, [xtl_real, ytl_real, xbr_real, ybr_real], (0, 255, 0), "Real")

                x_center_est, y_center_est = kf.x[0], kf.x[1]
                width, height = xbr_real - xtl_real, ybr_real - ytl_real
                xtl_est, ytl_est = x_center_est - width / 2, y_center_est - height / 2
                xbr_est, ybr_est = x_center_est + width / 2, y_center_est + height / 2
                draw_box(image, [xtl_est, ytl_est, xbr_est, ybr_est], (0, 0, 255), "Estimated")
        cv2.imshow('Image', image)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

def main():
    """
    Função principal que executa o fluxo de análise de imagem.
    """
    xml_path = 'archive/annotations.xml'
    xml_data = parse_xml(xml_path)
    train_data, _ = split_data(xml_data, 0.3)
    kalman_filters = process_annotations(train_data)
    process_images(train_data, kalman_filters)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
