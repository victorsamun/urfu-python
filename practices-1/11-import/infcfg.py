import configparser
import importlib.abc
import importlib.machinery
import os.path
import sys


def _config_to_dict(filename):
    config = configparser.ConfigParser()
    config.read(filename)

    result = {section: dict(values)
              for (section, values) in dict(config).items()}

    if not result['DEFAULT']:
        del result['DEFAULT']

    return result


class ConfigFinder(importlib.abc.MetaPathFinder):
    @classmethod
    def find_spec(cls, fullname, paths=None, target=None):
        name = fullname.rsplit('.')[-1]
        paths = paths or sys.path

        for path in paths:
            filename = os.path.join(path, f'{name}.inf')
            if os.path.isfile(filename):
                return importlib.machinery.ModuleSpec(
                    name=fullname,
                    loader=ConfigLoader(fullname, path, target),
                    origin=filename
                )


class ConfigLoader(importlib.abc.SourceLoader):
    def __init__(self, fullname, path, target):
        self.fullname = fullname
        self.path = path

    def get_data(self, path):
        name = path.rsplit('.')[-1]
        with open(os.path.join(self.path, f'{name}.inf')) as f:
            return f.read()

    def get_filename(self, fullname):
        return fullname

    def module_repr(self, module):
        return f'<module {module.__name__}>'

    def exec_module(self, module):
        filename = self.fullname.rsplit('.')[-1]
        filename = os.path.join(self.path, f'{filename}.inf')
        module.__dict__.update(_config_to_dict(filename))


sys.meta_path.append(ConfigFinder())
