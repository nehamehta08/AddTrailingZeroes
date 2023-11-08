import os

def cleanup_directories():
    processed_dir = 'media/processed'
    uploads_dir = 'media/uploads'
    temp_dir = 'media/temp_zip'

    for directory in [processed_dir, uploads_dir, temp_dir]:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f'Removed: {file_path}')

if __name__ == "__main__":
    cleanup_directories()
