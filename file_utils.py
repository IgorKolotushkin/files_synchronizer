from os import listdir, path

path_dir = 'files_syn/'

for file_name in listdir(path_dir):
    print(path.getmtime(path_dir + file_name))
