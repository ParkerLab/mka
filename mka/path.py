import argparse
import os
import os.path
import shutil
import tempfile


class FilePath():
    """Callable that checks a file path, suitable for use with argparse.add_argument(type=...)."""

    def __init__(self, require_existence=True, require_readable=True):
        self.require_existence = require_existence
        self.require_readable = require_readable

    def __call__(self, path):
        self.path = os.path.abspath(path)

        if self.require_existence and not os.path.isfile(path):
            msg = '{} is not a valid file.'.format(path)
            raise argparse.ArgumentTypeError(msg)

        if self.require_readable:
            try:
                open(path, 'r')
            except Exception as e:
                msg = '{} is not a readable file ({})'.format(path, e)
                raise argparse.ArgumentTypeError(msg)

        return path

    def __str__(self):
        return 'FilePath(require_existence={}, require_readable={}, path={}'.format(self.require_existence, self.require_readable, self.path)


def mkdir(path, mode=0o0755):
    """Construct a directory hierarchy using the given permissions.

    Returns the first level in the hierarchy that did not exist before
    invocation.

    """
    if not os.path.exists(path):
        components = splitpath(path)
        new_path = None
        for component in components:
            component = os.path.abspath(os.path.join('/', component))
            if os.path.exists(component):
                continue
            elif new_path is None:
                new_path = component
                break

        os.makedirs(path, mode)

        return new_path


def splitpath(path):
    head, tail = os.path.split(path)
    components = [path, head]
    while head != os.path.abspath('/'):
        head, tail = os.path.split(head)
        components.append(os.path.abspath(head))

    return list(reversed(components))


def symlink(src, dest, overwrite=False):
    if overwrite and os.path.exists(dest):
        os.unlink(dest)

    os.symlink(src, dest)
