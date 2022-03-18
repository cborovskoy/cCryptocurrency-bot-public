import os
import time


def get_new_and_old_charts(path):
    files = get_files_lst(path)
    return {'new': max(files, key=os.path.getctime),
            'old': min(files, key=os.path.getctime)}


def get_files_lst(path):
    files = os.listdir(path)
    files = [os.path.join(path, file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    return files



def delete_old_charts(path):
    # Оставляем только последние 2 графика
    while len(get_files_lst(path)) > 2:
        while True:
            try:
                os.remove(get_new_and_old_charts(path=path)['old'])
            except PermissionError:
                time.sleep(0.1)
                # print('PermissionError')
            except FileNotFoundError:
                print(f'{path}: FileNotFoundError')
                time.sleep(0.1)
            else:
                break
