"""Setup for the mailroom moduels."""

from setuptools import setup


setup(
    name="http-server",
    description="Echo server pinging back the input to the client",
    version=0.1,
    author="Amos Boldor, Marc Kessler-Wenicker",
    author_email='',
    license="MIT",
    package_dir={'': 'src'},
    py_modules=['server', 'client', 'concurrent_server', "gevent"],
    extras_require={
        "test": ["pytest", "pytest-watch", "pytest-cov", "tox", "gevent"]
    },
    entry_points={
        "console_scripts": [
            "server.py = server:main",
            "client.py = client:main"]
    }
)
