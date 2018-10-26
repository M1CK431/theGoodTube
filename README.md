# The good tube API
This product allow to use youtube-dl through a REST API.

The following features will be supported in v1.0:
* list supported sites (all sites supported by youtube-dl)
* display product version (the API itself and youtube-dl)
* get video informations
* download one or more videos
* list donwloading video(s) with details (title, progression, size, etc...)
* convert a video in any format supported by FFMPEG (see youtube-dl documentation)
* set default configuration options like download dir, default quality, etc...

## How to setup developement environment
/!\ You need at least Python 3.6 installed on your computer

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
python server.py
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

## Special thanks
The following links help me a lot to create this product:
* https://realpython.com/flask-connexion-rest-api/


## License
![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)  
This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)
