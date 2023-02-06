import os

import pytest
from anytree import Node, RenderTree

from jenkinsdiagram import app

filename_Jenkinsfile = 'Jenkinsfile'
subdir_name = 'pipelines'
filename_a = 'a.jenkinsfile'
filename_b = 'b.jenkinsfile'
filename_c = 'c.jenkinsfile'


def setup_test_files(tmp_path):
    file_toplevel = tmp_path / filename_Jenkinsfile
    subdir = tmp_path / subdir_name
    os.mkdir(subdir)

    file_a = subdir / filename_a
    file_b = subdir / filename_b
    file_c = subdir / filename_c

    file_toplevel.write_text("""
    // jenkins2diagram:toplevel
    build job: 'a'
    build job: 'b'
    """)
    file_a.write_text("")
    file_b.write_text("""
    build job: 'c'
    """)
    file_c.write_text("")

    return [file_toplevel, file_a, file_b, file_c]


def test_can_find_relevant_files(tmp_path):
    expected_files = setup_test_files(tmp_path)

    file_nonroot_Jenkinsfile = tmp_path / subdir_name / filename_Jenkinsfile
    file_nonroot_Jenkinsfile.write_text("")
    expected_files.append(file_nonroot_Jenkinsfile)

    file_to_ignore = tmp_path / 'ignoreMe.java'
    file_to_ignore.write_text('spice')

    paths = app.list_file_paths(tmp_path)
    assert sorted(paths) == sorted(expected_files)


def test_can_filter_toplevel_pipelines(tmp_path):
    setup_test_files(tmp_path)

    another_toplevel_file = tmp_path / subdir_name / 'another_toplevel.jenkinsfile'
    another_toplevel_file.write_text('// jenkins2diagram:toplevel')

    expected_paths = [
        tmp_path / filename_Jenkinsfile,
        tmp_path / subdir_name / another_toplevel_file.name
    ]
    provided_paths = app.list_file_paths(tmp_path)
    filtered_paths = app.filter_toplevel_files(provided_paths)
    assert filtered_paths == expected_paths


def test_can_find_job_inside_pipeline(tmp_path):
    setup_test_files(tmp_path)
    file_with_job = tmp_path / subdir_name / filename_b
    expected_inner_jobs = ['c']

    inner_jobs = app.find_inner_jobs(file_with_job)

    assert inner_jobs == expected_inner_jobs


def test_can_generate_tree(tmp_path):
    setup_test_files(tmp_path)

    jenkinsfile = Node("Jenkinsfile")
    Node("a", parent=jenkinsfile)
    b = Node("b", parent=jenkinsfile)
    Node("c", parent=b)
    expected_tree = RenderTree(jenkinsfile)

    paths = app.list_file_paths(tmp_path)
    toplevel_files = app.filter_toplevel_files(paths)
    trees = []
    for toplevel_path in toplevel_files:
        tree = app.generate_tree(toplevel_path, paths)
        trees.append(tree)

    generated_tree = RenderTree(trees[0])

    assert len(trees) == 1
    assert generated_tree.__str__() == expected_tree.__str__()


def test_can_convert_int_to_letter():
    assert app.get_key(25) == 'Z'
    assert app.get_key(0) == 'A'
    assert app.get_key(1) == 'B'


def test_can_convert_tree_to_mermaid(tmp_path):
    setup_test_files(tmp_path)
    paths = app.list_file_paths(tmp_path)
    toplevel_files = app.filter_toplevel_files(paths)
    trees = []
    for toplevel_path in toplevel_files:
        tree = app.generate_tree(toplevel_path, paths)
        trees.append(tree)
    tree = trees[0]

    expected_mermaid = """```mermaid
graph TD
    Z[Jenkinsfile]
    Z[Jenkinsfile] --> A[a]
    Z[Jenkinsfile] --> B[b]
    B[b] --> C[c]
```"""
    # make the newlines here be os-specific so tests work in GitHub Action (Ubuntu) + local (Windows)

    mermaid = app.convert_tree_to_mermaid(tree)
    assert mermaid == expected_mermaid


test_lines = [
    ("build job:'a')", 'a'),  # OK with single job name
    ("build(job:'b')", 'b'),  # OK with brackets
    ("build( job: 'c')", 'c'),  # OK with spaces
    ('build(job: "d")', 'd'),  # OK with double quotes
    ('', None)  # Returns None if not found
]


@pytest.mark.parametrize("line,expected", test_lines)
def test_can_find_job_on_line(line, expected):
    assert app.find_job_on_line(line) == expected
