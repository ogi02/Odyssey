# Odyssey
A website like Patreon, built by two 11 graders with Flask and Svelte JS.

## Requirements
 - [Python](https://www.python.org/) - any version >= 3 \
 - [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) - compatible for Python 3 \
 - [Node JS](https://nodejs.org/en/), used for its [NPM](https://www.npmjs.com/)(Node Package Manager) - developed with 6.12.0 \

### Operating Systems
This project was developed on Mac OS Catalina and Ubuntu 19.10, but it is compatible with Windows as well, as long as you can install and set the paths for the required software.

### To Run
Go to Terminal and type the following commands: 
```
cd Odyssey/odyssey/api
make
```

The Makefile runs the following script:
```
all:
	make flask & make svelte

flask:
	pipenv install && pipenv run flask run

svelte:
	cd client/ && npm install && npm run autobuild
```
&& -> synchronous,
& -> asynchronous, so that both the Flask server and the Svelte front-end are started.

### To Edit
Go to Terminal and type the following commands: 
```
cd Odyssey/odyssey/api
pipenv install
pipenv shell
cd client/
npm install
```
'pipenv' will install any libraries used in Flask, whereas 'npm' will install any libraries used in Svelte JS.

### Commit Messages Formatting
 - [Update] "commit message"
 - [Remove] "commit message"
 - [Fix] "commit message"
 - [New] "commit message"

### Libraries
[Flask](https://flask.palletsprojects.com/en/1.1.x/) for backend \
[Svelte JS](https://svelte.dev/) for frontend and REST API \
[PyMongo](https://api.mongodb.com/python/current/tutorial.html) as database \
[Python Dotenv](https://pypi.org/project/python-dotenv/) for app configurations

### Creators
[Gabriela Yoncheva](https://github.com/GabrielaY) \
[Ognian Baruh](https://github.com/ogi02)

### About
[Official assignment](https://docs.google.com/document/d/1fe4PTeQvuJQCtzLAepiWgYKQRrgO0HffOD3cP5iOwkI/edit?usp=sharing) \
[Additional notes](https://docs.google.com/document/d/1MGU3UjkklhmtIZYOXibMGOLQSNI5sJdpi29l_KBRsfU/edit) \
[Overview](https://docs.google.com/spreadsheets/d/19rgsBmh61TQRARmx8KPktfGFi1IK6kYtLRE6ENJNaMM/edit#gid=0)
