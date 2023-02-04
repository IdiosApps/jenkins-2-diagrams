import os


def list_files(src):
    files = []

    if os.path.exists(src / 'Jenkinsfile'):
        files.append('Jenkinsfile')

    for path in src.rglob('*.jenkinsfile'):
        print(path.name)
        files.append(path.name)

    return files


