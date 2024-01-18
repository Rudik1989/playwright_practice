from os import path

from setuptools import setup


def package_env(file_name, strict=False):
    file_path = path.join(path.dirname(__file__), file_name)
    if path.exists(file_path) or strict:
        return open(file_path).read()
    else:
        return ''


def parse_requirements(filename):
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == '__main__':
    setup(
        name='Shared',
        version='1.0.0',
        description='Shared automation testing framework.',
        long_description=package_env('README.md'),
        author='Volodymyr Rudyshyn',
        author_email='vladymyr.rudyshyn@gmail.com',
        packages=['shared'],
        include_package_data=True,
        install_requires=parse_requirements('requirements.txt'),
        zip_safe=False,
        entry_points={
            'pytest11': ['shared = shared.runner.plugin:SharedRunnerPlugin']
        }
    )
