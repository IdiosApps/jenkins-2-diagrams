import os

from anytree import Node, RenderTree

import app

filename_toplevel = 'Jenkinsfile'
subdir_name = 'pipelines'
filename_a = 'a.jenkinsfile'
filename_b = 'b.jenkinsfile'
filename_c = 'c.jenkinsfile'


def setup_test_files(tmp_path):
    file_toplevel = tmp_path / filename_toplevel
    subdir = tmp_path / subdir_name
    os.mkdir(subdir)

    file_a = subdir / filename_a
    file_b = subdir / filename_b
    file_c = subdir / filename_c

    file_toplevel.write_text("""
    // jenkins2diagram:toplevel
    job: a
    job: b
    """)
    file_a.write_text("")
    file_b.write_text("""
    job: c
    """)
    file_c.write_text("")


def test_can_find_relevant_files(tmp_path):
    setup_test_files(tmp_path)

    file_to_ignore = tmp_path / 'ignoreMe.java'
    file_to_ignore.write_text('spice')

    expected_files = [filename_toplevel, filename_a, filename_b, filename_c]
    paths = app.list_file_paths(tmp_path)
    files = [path.name for path in paths]
    assert files == expected_files


def test_can_filter_toplevel_pipelines(tmp_path):
    setup_test_files(tmp_path)

    another_toplevel_file = tmp_path / subdir_name / 'another_toplevel.jenkinsfile'
    another_toplevel_file.write_text('// jenkins2diagram:toplevel')

    expected_paths = [
        tmp_path / filename_toplevel,
        tmp_path / subdir_name / another_toplevel_file.name
    ]
    provided_paths = app.list_file_paths(tmp_path)
    filtered_paths = app.filter_toplevel_files(provided_paths)
    assert filtered_paths == expected_paths


def test_can_generate_tree(tmp_path):
    setup_test_files(tmp_path)

    paths = app.list_file_paths(tmp_path)

    jenkinsfile = Node("Jenkinsfile")
    a = Node("a", parent=jenkinsfile)
    b = Node("b", parent=jenkinsfile)
    c = Node("c", parent=b)

    for pre, fill, node in RenderTree(jenkinsfile):
        print("%s%s" % (pre, node.name))
    expected_tree = RenderTree(jenkinsfile)
    tree = app.generate_tree()
    
    assert RenderTree(tree) == expected_tree
