from setuptools import setup
from cyberpy import __version__

try:
    import pypandoc
except ImportError:
    pypandoc = None


def readme():
    with open('README.md', 'r') as f:
        readme_md = f.read()
        if pypandoc:
            readme_rst = pypandoc.convert(readme_md, 'rst', format='md')
            return readme_rst
        else:
            return readme_md


setup(
    name='cyberpy',
    version=__version__,
    description='A secure way to share secrets over a local network.',
    long_description=readme(),
    url='http://github.com/sirMackk/cyberpy',
    author='Matt O.',
    author_email='matt@mattscodecave.com',
    license='MPL',
    keywords='async secret lan sharing',
    packages=['cyberpy'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cyberpy = cyberpy.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Topic :: Software Development',
    ],
)
