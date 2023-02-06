from distutils.core import setup

setup(
    name='jenkinsdiagram',
    version='1.0.0',
    packages=['jenkinsdiagram'],
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
    ]
)
