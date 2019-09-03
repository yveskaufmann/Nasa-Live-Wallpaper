import setuptools
import configparser

with open("README.md", "r") as fh:
    long_description = fh.read()

config = configparser.ConfigParser()
config.read('Pipfile')
requires = ["".join(l).replace("\"", "") for l in config.items('packages')]

setuptools.setup(
    name="nasa-live-wallpaper",
    version="0.0.1",
    author="Yves Kaufmann",
    author_email="yves@no-mail.com",
    description="Command line utility that, displays NASA's images of the day on your wallpaper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yveskaufmann/Nasa-Live-Wallpaper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requires,
    entry_points = {
        'console_scripts': ['nasa-live-wallpaper=nasa_wallpaper.__main__:main'],
    }

)