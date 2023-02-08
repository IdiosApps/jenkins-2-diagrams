from enum import Enum

from anytree import Node

toplevel_marker = '// jenkins2diagram:toplevel'


def list_file_paths(src):
    files = []

    for path in src.rglob('**/Jenkinsfile'):
        files.append(path)

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


def find_job_on_line(line):
    if 'job:' in line:
        # https://stackoverflow.com/a/2076399/4261132 Thanks Roman
        params_single_quote = line.split("'")[1::2]
        if params_single_quote:
            return params_single_quote[0]
        # Note: strings like "${jobName}" won't ever work
        params_double_quote = line.split('"')[1::2]
        if params_double_quote:
            return params_double_quote[0]


def find_inner_jobs(pipeline_path):
    file = open(pipeline_path, 'r')
    lines = file.readlines()

    inner_job_names = []
    for line in lines:
        job = find_job_on_line(line)
        if job is not None:
            inner_job_names.append(job)

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

    root_node = Node(toplevel_path.stem)
    recurse_nodes(toplevel_path, root_node)

    return root_node


# https://mermaid.live/ sample Flow diagram increments letters A, B, C...
def get_key(letter_index):
    return chr(65 + letter_index)


def convert_tree_to_mermaid(tree):
    tree.key = get_key(25)
    letter_index = 0
    for descendant in tree.descendants:
        descendant.key = get_key(letter_index)
        letter_index += 1

    lines = [f'{tree.key}[{tree.name}]']
    for descendant in tree.descendants:
        lines.append(f'{descendant.parent.key}[{descendant.parent.name}] --> {descendant.key}[{descendant.name}]')

    separator = "\n    "

    return f"""```mermaid
graph TD
    {separator.join(lines)}
```
    """.rstrip()


class OutputType(str, Enum):
    md = "md"
    svg = "svg"
    png = "png"
    pdf = "pdf"
    all_files = "all-files"
