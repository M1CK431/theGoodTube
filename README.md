# The good tube API

This product allow to use youtube-dl through a REST API.

The following features will be supported in v1.0:

- list supported sites (all sites supported by youtube-dl)
- display product version (the API itself and youtube-dl)
- get video informations
- download one or more videos
- list downloading video(s) with details (title, progression, size, etc...)
- convert a video in any format supported by FFMPEG (see youtube-dl documentation)
- set default configuration options like download dir, default quality, etc...

## How to use it

/!\ You need at least Python 3.7 installed on your computer

### Create new python isolate environment

```bash
python -m venv env
source env/bin/activate
pip install --upgrade pip
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Start the server

```bash
python run.py
```

## How to update requirements

I want to always use upstream third party libraries so I need to only keep package name in my requirements.txt file.

```bash
pip freeze | grep -o '^\([[:alnum:]]\|-\)*' > requirements.txt
```

Then to update all packages to the latest version:

```bash
pip install --upgrade -r requirements.txt
```

## Known issues

As it's my first API and Python app, I'm pretty sure that a lot of things should be better.

The main current issue is that I don't know how to run it in production mode.
I have try to install and use gunicorn but I have an error message about worker timeout in console and I don't know how to solve it.
**Any help with this issue will be greatly appreciated**

Also, for now, there is a technical limitation which forbid to choose the destination name of downloaded files.
This is because youtube-dl doesn't provide an easy way to identify the download in the progress hook (and there is now way to pass extra params to the hook function). I don't plan to fix this until v1.0 release.

## License

![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)
