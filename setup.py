import os

from setuptools import setup, find_packages

version = open('VERSION').read().strip()
long_description = open("README.rst").read()

install_requires = [
    'Django>=1.6,<1.8',
    'django-nose>=1.3,<2',
    'django-redis>=3.8.1,<4',
    'six'
]

try:
    import sphinx
    from sphinx.setup_command import BuildDoc
    import sphinx.apidoc

    class Sphinx(BuildDoc):

        def run(self):
            src_dir = (self.distribution.package_dir or {'': ''})['']
            src_dir = os.path.join(os.getcwd(), src_dir)
            sphinx.apidoc.main(
                ['', '-f', '-o', os.path.join(self.source_dir, '_apidoc'),
                 src_dir])
            BuildDoc.run(self)
except ImportError:
    sphinx = None

setup(
    name="django-cache-management",
    version=version,
    packages=find_packages(),
    author="Louis-Dominique Dubeau",
    author_email="ldd@lddubeau.com",
    description="Cache management for Django.",
    long_description=long_description,
    license="MPL 2.0",
    keywords=["Django", "caching"],
    url="https://github.com/lddubeau/django-cache-management",
    install_requires=install_requires,
    # use_2to3=True,
    classifiers=[
        "Programming Language :: Python",
        #"Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX",
        "Framework :: Django",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    setup_requires=['sphinx'],
    cmdclass={'sphinx': Sphinx} if sphinx is not None else {}
)
