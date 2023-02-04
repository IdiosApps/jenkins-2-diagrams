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

    inner_job_names = []
    for line in lines:
        if 'job:' in line:
            # https://stackoverflow.com/a/2076399/4261132 Thanks Roman
            parameters = line.split("'")[1::2]
            # assume the job names are the first param
            # can add more tests & better handling later
            inner_job_names.append(parameters[0])

    return inner_job_names


def generate_tree(toplevel_path, all_paths):
    def recurse_nodes(path, parent_node):
        inner_job_names = find_inner_jobs(path)
        inner_job_paths = list(filter(lambda path: path.stem in inner_job_names, all_paths))

        if len(inner_job_names) == 0:
            return

        for inner_job_path in inner_job_paths:
            node = Node(inner_job_path.stem, parent=parent_node)
            recurse_nodes(inner_job_path, node)

    root_node = Node(toplevel_path.name)
    recurse_nodes(toplevel_path, root_node)

    return root_node


# https://mermaid.live/ sample Flow diagram increments letters A, B, C...
def convert_int_to_letter(int):
    return chr(65 + int)


def convert_tree_to_mermaid(tree):
    mermaid = "graph TD\n"
    letter_index = 0

    txt = f'{convert_int_to_letter(letter_index)}[{tree.name}]'
    return mermaid
