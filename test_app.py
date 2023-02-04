import os

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
    assert app.list_files(tmp_path) == expected_files



