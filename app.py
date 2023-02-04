import os


def list_file_paths(src):
    files = []

    jenkinsfile_path = src / 'Jenkinsfile'
    if os.path.exists(jenkinsfile_path):
        files.append(jenkinsfile_path)

    for path in src.rglob('*.jenkinsfile'):
        files.append(path)

    return files


def filter_toplevel_files(files):
    return files
