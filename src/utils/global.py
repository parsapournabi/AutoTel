import os


def iter_files(root, extensions=None):
    """
    Reading all existing files recursively from root path
    :param root: path of specific directory
    :param extensions: file filtering for example (".jpg", ".cpp")
    :return: generator of the files paths
    """
    with os.scandir(root) as it:
        for entry in it:
            if entry.is_dir(follow_symlinks=False):
                yield from iter_files(entry.path, extensions)
            elif entry.is_file(follow_symlinks=False):
                if extensions is None or entry.name.endswith(extensions):
                    yield entry.path


if __name__ == '__main__':
    # for file in iter_files("qml", (".qml", ".js")):
    #     print(file)
    pics = list(iter_files(os.path.join(os.path.expanduser("~"), "Pictures/"), (".jpg")))

    print(len(pics), pics)
