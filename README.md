# wthr

A minimal, cross-platform weather CLI tool. This program is meant to be extremely simple, fast, and lightweight.

### Install

Clone this repository. Install requirements.txt

### Running

Fetch the current weather at your current location
```console
python3 main.py
```

Fetch the weather for the next 12 hours at your current location
```console
python3 main.py -f
```

Save a city, so that you can view in the future
```console
python3 main.py -s
```

Fetch the weather of a city that you have saved before
```console
python3 main.py -l NewYork
```

