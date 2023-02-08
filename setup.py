from setuptools import setup, find_packages

setup(
    name='jenkinsdiagram',
    version='1.0.2',
    packages=find_packages(),
    url='https://github.com/IdiosApps/jenkinsdiagram',
    license='MIT',
    author='IdiosApps',
    author_email='IdiosApps@users.noreply.github.com',
    description='Generate mermaid diagrams from Jenkins pipelines',
    install_requires=[
        "anytree",
        "click",
        "colorama",
        "commonmark",
        "Pygments",
        "rich",
        "shellingham",
        "six",
        "typer",
    ],
    entry_points="""
        [console_scripts]
        jenkinsdiagram=jenkinsdiagram.main:main
    """,
)
