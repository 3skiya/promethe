import os

def save_and_print_directory_structure(root_dir, output_file):
    with open(output_file, 'w') as f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            level = dirpath.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write('{}{}/\n'.format(indent, os.path.basename(dirpath)))
            print('{}{}/'.format(indent, os.path.basename(dirpath)))
            sub_indent = ' ' * 4 * (level + 1)
            for filename in filenames:
                f.write('{}{}\n'.format(sub_indent, filename))
                print('{}{}'.format(sub_indent, filename))

if __name__ == "__main__":
    root_directory = '/root/Crypto/Prometheus'  # Çalışma dizininizi buraya yazın
    output_filename = 'Dizin_yapısı.txt'
    save_and_print_directory_structure(root_directory, output_filename)
