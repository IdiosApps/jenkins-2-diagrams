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


def find_inner_jobs(pipeline_path):
    file = open(pipeline_path, 'r')
    lines = file.readlines()

    inner_jobs = []
    for line in lines:
        if 'job:' in line:
            # https://stackoverflow.com/a/2076399/4261132 Thanks Roman
            parameters = line.split("'")[1::2]
            # assume the job names are the first param
            # can add more tests & better handling later
            inner_jobs.append(parameters[0])

    return inner_jobs


def generate_tree(toplevel_path):
    return Node('x')
