import sys, os, shutil

def get_cordenadas(box):
    cordenadas = []
    x = y = ''
    num = 'x'
    for i in box:
        if i.isnumeric():
            if num == 'x':
                x = (x + i)
            else:
                y = (y + i)
        elif i == ',':
            num = 'y'
        elif i == ' ':
            cordenadas.append((int(x), int(y)))
            num = 'x'
            x = y = ''
        else:
            continue

    cordenadas.append((int(x), int(y)))
    return cordenadas

def normalize_coordinates(box):
    image_width = 1280
    image_height = 720

    cordenadas  = get_cordenadas(box=box)

    box_x_left = cordenadas[0][0]
    box_y_top = cordenadas[0][1]
    box_width = cordenadas[1][0] - box_x_left
    box_height = cordenadas[2][1] - cordenadas[1][1]

    x_center = (box_x_left + box_width / 2) / image_width
    y_center = (box_y_top + box_height / 2) / image_height
    width = box_width / image_width
    height = box_height / image_height
    return f'{x_center} {y_center} {width} {height}'


def main(path:str):
    
    # diretórios de destino
    dataset_path = f'{path}/../dataset'
    images_path_train = f'{dataset_path}/images/train'
    label_path_train = f'{dataset_path}/labels/train'
    images_path_val = f'{dataset_path}/images/val'
    label_path_val = f'{dataset_path}/labels/val'

    # Cria os diretórios
    os.mkdir(dataset_path) if not os.path.exists(dataset_path) else None
    os.makedirs(images_path_train) if not os.path.exists(images_path_train) else None
    os.makedirs(label_path_train) if not os.path.exists(label_path_train) else None
    os.makedirs(images_path_val) if not os.path.exists(images_path_val) else None
    os.makedirs(label_path_val) if not os.path.exists(label_path_val) else None

    # Lê arquivo com divisão
    file_split = open(f'{path}/split.txt', 'r')
    file_split_lines = file_split.readlines()
    file_split.close()

    for line in file_split_lines:
        line = line.split('/')

        if line[2] not in ['cars-br', 'cars-me']: # ignora placas de moto
            continue

        img_name, img_type = line[-1].split(';')
        label_name = img_name.replace('.jpg', '.txt')

        # Obtém o tipo de imagem (treinamento, teste ou validação)
        if img_type == 'training\n' or img_type == 'testing\n':
            destino_imagem = images_path_train
            destino_label = label_path_train
        elif img_type == 'validation\n':
            destino_imagem = images_path_val
            destino_label =label_path_val
        else:
            continue

        # copia a imagem
        imagem_original = f'{path}/images/{line[2]}/{img_name}'
        shutil.copyfile(imagem_original, f'{destino_imagem}/{img_name}')

        # obtém os cantos
        label_file_dest = open(f"{imagem_original.replace('.jpg', '.txt')}", 'r')
        cantos = label_file_dest.readlines()[-1]
        label_file_dest.close()

        normalized_box = normalize_coordinates(cantos[9:])

        # escreve os cantos
        label_file_origin = open(f'{destino_label}/{label_name}', 'w')
        label_file_origin.write(f'0 {normalized_box}')
        label_file_origin.close()



if __name__ == '__main__':

    if (len(sys.argv) <= 1):
        print("Informe o caminho para a pasta raíz do dataset como primeiro parâmetro.")
        exit()
    
    if os.path.exists(sys.argv[1]):
        path = sys.argv[1]

        main(path)

    else:
        print("Diretório inválido.")