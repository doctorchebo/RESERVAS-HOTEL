from django.core.exceptions import ValidationError

def validar_tamaño_imagen(file):
    max_file_size_kb = 5000

    if file.size>max_file_size_kb*1024:
        print('VALIDATION')
        raise ValidationError(f'El archivo no puede tener más de {max_file_size_kb} KB')