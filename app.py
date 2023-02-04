import os

from anytree import Node

toplevel_marker = '// jenkins2diagram:toplevel'


def list_file_paths(src):
    files = []

    jenkinsfile_path = src / 'Jenkinsfile'
    if os.path.exists(jenkinsfile_path):
        files.append(jenkinsfile_path)

    for path in src.rglob('*.jenkinsfile'):
        files.append(path)

    return files


def filter_toplevel_files(files):
    toplevel_files = []
    for file in files:
        content = file.read_text()
        if toplevel_marker in content:
            toplevel_files.append(file)

    return toplevel_files


def generate_tree():
    return Node('x')
