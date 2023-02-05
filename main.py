from pathlib import Path
from typing import Optional

import typer


def main(
        path: Optional[Path] = typer.Option(default=None,
                                            case_sensitive=False,
                                            help="""Path to repository
                                             | Default: current working directory
                                             | Example: jenkinsdiagram --path ~/IdeaProjects/myrepo""",
                                            show_default=False
                                            ),
        # folders: Optional[str] = typer.Option(default=None,
        #                                       help="Folders to scan for .jenkinsfiles",
        #                                       show_default=False
        #                                       ),
        output: Optional[Path] = typer.Option(default="stdout",
                                              help="Path or Filename for output. Example:",
                                              ),
):
    """
    Scans Jenkins pipelines in a repository and generates Mermaid flow graphs
    """

    if path is None:
        current_working_directory = "cwd"
        print(f"PATH: Scanning from current directory, {current_working_directory}")
    elif path.is_dir():
        print("Path is a directory, will use all its config files")


if __name__ == "__main__":
    typer.run(main)
