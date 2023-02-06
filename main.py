import os
import subprocess
from pathlib import Path
from typing import Optional

import typer

import app

__version__ = "1.0.0"


def version_callback(value: bool):
    if value:
        print(f"""jenkinsdiagram version: {__version__}
        The latest available version is ???
        https://github.com/IdiosApps/jenkinsdiagrams/releases""")
        raise typer.Exit()


def main(
        version: Optional[bool] = typer.Option(
            None, "--version",
            callback=version_callback,
            help= "Prints the version"
        ),
        path: Optional[Path] = typer.Option(default=None,
                                            case_sensitive=False,
                                            help="""Path to repository
                                             | Default: current working directory
                                             | Example: jenkinsdiagram --path ~/IdeaProjects/myrepo
                                             """,
                                            show_default=False
                                            ),
        output_type: Optional[app.OutputType] = typer.Option(default=None,
                                                             help="""Output type
                                              | Default: print to stdout
                                              | Example: jenkinsdiagram --output-type markdown
                                              | Note: svg is broken, use png: https://github.com/mermaid-js/mermaid-cli/issues/112
                                              """,
                                                             show_default=False,
                                                             ),
        output_path: Optional[Path] = typer.Option(default=None,
                                                   help="""Path to write files to
                                              | Default: stdout
                                              | Example: jenkinsdiagram --output_path ~/IdeaProjects/myrepo/docs/jenkins/diagrams
                                              """,
                                                   show_default=False,
                                                   ),
        # folders: Optional[str] = typer.Option(default=None,
        #                                       help="Folders to scan for .jenkinsfiles",
        #                                       show_default=False
        #                                       ),
):
    """
    Scans Jenkins pipelines in a repository and generates Mermaid flow graphs
    """

    checked_path = find_input_path(path)
    check_output_path(output_path)

    paths = app.list_file_paths(checked_path)
    toplevel_files = app.filter_toplevel_files(paths)

    if len(toplevel_files) == 0:
        raise Exception("""Could not find any toplevel Jenkinsfile / *.jenkinsfiles
        Please annotate your toplevel Jenkins pipelines with:
        //  jenkins2diagram:toplevel
        """)

    for toplevel_path in toplevel_files:
        tree = app.generate_tree(toplevel_path, paths)
        render_trees(tree, output_path, output_type)


# todo refactors - move helpers out of app.py and main.py, name appropriately, etc.


def find_input_path(path):
    if path is None:
        path = Path.cwd()
    if not path.exists():
        raise Exception(f"Couldn't find path: {path}")
    elif path.is_dir() and not path.is_absolute():
        path = Path.cwd() / path
    print(f"Scanning files in path: {path}")
    return path


def check_output_path(path):
    if path is not None and not path.exists():
        raise Exception(f"""Couldn't find path: {path}
        Please check this is the correct path, and create it if it doesn't exist""")


def render_trees(tree, output_path, output_type):
    mermaid = app.convert_tree_to_mermaid(tree)
    name = tree.name + '-mermaid'

    if output_type is None:
        print(f"Mermaid flow diagram for {name}:")
        print(f"{mermaid}\n")
        return

    if output_type == app.OutputType.md:
        write_markdown_file(output_path, name, mermaid)
        return

    check_mermaid_cli_installation()
    # Rather than dealing with stdout, I'm being a bit lazy and converting files
    filepath_markdown = write_markdown_file(output_path, name, mermaid)

    if output_type == app.OutputType.svg or output_type == app.OutputType.png or output_type == app.OutputType.pdf:
        write_image_files(filepath_markdown, output_type.name)
        os.remove(filepath_markdown)
        return

    write_image_files(filepath_markdown, app.OutputType.png.name)
    write_image_files(filepath_markdown, app.OutputType.svg.name)
    write_image_files(filepath_markdown, app.OutputType.pdf.name)


def write_markdown_file(output_path, name, mermaid):
    filepath = (output_path / name).with_suffix('.md')
    filepath.touch()
    filepath.write_text(mermaid)
    return filepath


def write_image_files(filepath_markdown, output_ext):
    filepath_image = filepath_markdown.with_suffix(f".{output_ext}")
    command = f"mmdc -i {filepath_markdown} -o {filepath_image}"
    os.system(command)


def check_mermaid_cli_installation():
    # command = f"mmdc --version"
    # return_code = os.system(command)
    result = subprocess.run('mmdc --version', shell=True, stdout=subprocess.DEVNULL)

    if result.returncode != 0:
        raise Exception("""Could not find mmdc
         Please check installation: https://github.com/mermaid-js/mermaid-cli#installation
         If installed, consider restarting your PC (it may fix the PATH)""")


if __name__ == "__main__":
    typer.run(main)
