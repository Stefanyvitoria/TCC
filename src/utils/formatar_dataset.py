import sys, os, shutil

def main(path):
    
    # diretórios de destino
    dataset_path = f'{path}/../dataset1'
    images_path_train = f'{dataset_path}/images/train'
    label_path_train = f'{dataset_path}/labels/train'
    images_path_val = f'{dataset_path}/images/val'
    label_path_val = f'{dataset_path}/labels/val'
    images_path_test = f'{dataset_path}/images/test'
    label_path_test = f'{dataset_path}/labels/test'

    # Cria os diretórios
    os.mkdir(dataset_path) if not os.path.exists(dataset_path) else None
    os.makedirs(images_path_train) if not os.path.exists(images_path_train) else None
    os.makedirs(label_path_train) if not os.path.exists(label_path_train) else None
    os.makedirs(images_path_val) if not os.path.exists(images_path_val) else None
    os.makedirs(label_path_val) if not os.path.exists(label_path_val) else None
    os.makedirs(images_path_test) if not os.path.exists(images_path_test) else None
    os.makedirs(label_path_test) if not os.path.exists(label_path_test) else None

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
        if img_type == 'training\n':
            destino_imagem = images_path_train
            destino_label = label_path_train
        elif img_type == 'validation\n':
            destino_imagem = images_path_val
            destino_label =label_path_val
        else:
            destino_imagem = images_path_test
            destino_label = label_path_test

        # copia a imagem
        imagem_original = f'{path}/images/{line[2]}/{img_name}'
        shutil.copyfile(imagem_original, f'{destino_imagem}/{img_name}')

        # obtém os cantos
        label_file_dest = open(f"{imagem_original.replace('.jpg', '.txt')}", 'r')
        cantos = label_file_dest.readlines()[-1]
        label_file_dest.close()

        # escreve os cantos
        label_file_origin = open(f'{destino_label}/{label_name}', 'w')
        label_file_origin.write(f'0 {cantos[9:]}'.replace(',', '.'))
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