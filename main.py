import os
from pathlib import Path
from typing import Optional

import typer

import app


def main(
        path: Optional[Path] = typer.Option(default=None,
                                            case_sensitive=False,
                                            help="""Path to repository
                                             | Default: current working directory
                                             | Example: jenkinsdiagram --path ~/IdeaProjects/myrepo
                                             """,
                                            show_default=False
                                            ),
        output_type: Optional[app.OutputType] = typer.Option(default=app.OutputType.stdout,
                                                             help="""Output type
                                              | Default: stdout
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

    checked_path = find_path(path)

    paths = app.list_file_paths(checked_path)
    toplevel_files = app.filter_toplevel_files(paths)

    for toplevel_path in toplevel_files:
        tree = app.generate_tree(toplevel_path, paths)
        render_trees(tree, output_path, output_type)


def find_path(path):
    if path is None:
        path = Path.cwd()
    if not path.exists():
        raise Exception(f"Couldn't find path: {path}")
    elif path.is_dir() and not path.is_absolute():
        path = Path.cwd() / path
    print(f"Scanning files in path: {path}")
    return path


def render_trees(tree, output_path, output_type):
    mermaid = app.convert_tree_to_mermaid(tree)
    name = tree.name + '-mermaid'
    if output_type is None:
        print(f"Mermaid flow diagram for ${name}:")
        print(f"{mermaid}\n")
    elif output_type == app.OutputType.md:
        write_markdown_file(output_path, name, mermaid)
    elif output_type == app.OutputType.md or output_type == app.OutputType.png:
        validate_mermaid_cli_installation()
        # Rather than dealing with stdout, I'm being a bit lazy and converting files
        filepath_markdown = write_markdown_file(output_path, name, mermaid)
        filepath_image = (output_path / name).with_suffix(f".{output_type.name}")
        command = f"mmdc -i {filepath_markdown} -o {filepath_image}"
        # command = "npm update"
        os.system(command)


def write_markdown_file(output_path, name, mermaid):
    filepath = (output_path / name).with_suffix('.md')
    filepath.touch()
    filepath.write_text(mermaid)
    return filepath


def validate_mermaid_cli_installation():
    pass


if __name__ == "__main__":
    typer.run(main)
