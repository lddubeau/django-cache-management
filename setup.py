import os

from setuptools import setup, find_packages

version = open('django_cache_management/VERSION').read().strip()
long_description = open("README.rst").read()

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
    install_requires=[
        'Django>=1.11',
    ],
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    setup_requires=['sphinx'],
    include_package_data=True,
    cmdclass={'sphinx': Sphinx} if sphinx is not None else {}
)
