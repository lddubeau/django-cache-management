from setuptools import setup, find_packages

version = open('VERSION').read().strip()

install_requires = [
    'django-nose>=1.3,<2',
    'django-redis>=3.8.1,<4',
    'six'
]

setup(
    name="django-cache-management",
    version=version,
    packages=find_packages(),
    author="Louis-Dominique Dubeau",
    author_email="ldd@lddubeau.com",
    description="Cache management for Django.",
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
)
