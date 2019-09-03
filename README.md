# Nasa Live Wallpaper

Is a python script, that fetches NASA Images of the day
and display each on your desktop background for
a specific amount of seconds. 

## Dev Requirements

Before you can install the dependencies with pip, you have to install some os specific requirements.

### Mac

```sh
xcode-select –install
brew install libtiff libjpeg webp littlecms
```

### Ubuntu

```sh
sudo apt-get install python3-dev python3-setuptools \
libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev \
liblcms1-dev libwebp-dev tcl8.5-dev tk8.5-dev \
build-dep
```

### Dev Setup

```sh
pipenv --python 3.6
pipenv install
pipenv shell
```
