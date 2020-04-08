import functools
import itertools
import os.path
import sys


def project_stats(path, extensions):
    """
    Вернуть число строк в исходниках проекта.

    Файлами, входящими в проект, считаются все файлы
    в папке ``path`` (и подпапках), имеющие расширение
    из множества ``extensions``.
    """
    return total_number_of_lines(
        with_extensions(extensions, iter_filenames(path)))


def total_number_of_lines(filenames):
    """
    Вернуть общее число строк в файлах ``filenames``.
    """
    return sum(map(number_of_lines, filenames))


def number_of_lines(filename):
    """
    Вернуть число строк в файле.
    """
    with open(filename, encoding='utf8', errors='ignore') as f:
        return sum(map(lambda _: 1, f))


def iter_filenames(path):
    """
    Итератор по именам файлов в дереве.
    """
    return itertools.chain.from_iterable(
        itertools.starmap(
            lambda dp, _, fn: map(functools.partial(os.path.join, dp), fn),
            os.walk(path)))


def with_extensions(extensions, filenames):
    """
    Оставить из итератора ``filenames`` только
    имена файлов, у которых расширение - одно из ``extensions``.
    """
    extensions = set(extensions)
    return filter(lambda fn: get_extension(fn) in extensions, filenames)


def get_extension(filename):
    """ Вернуть расширение файла """
    return os.path.splitext(filename)[1]


def print_usage():
    print("Usage: python source_stats.py <project_path>")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)

    project_path = sys.argv[1]
    print(project_stats(project_path, {'.cs'}))
