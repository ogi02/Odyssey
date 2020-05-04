# Odyssey

A website like Patreon, built by two 11 graders with Flask and Svelte JS.

### Requirements

- [Python](https://www.python.org/) - any version of Python 3
- [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/) - compatible for Python 3
- [Node JS](https://nodejs.org/en/), used for its [NPM](https://www.npmjs.com/)(Node Package Manager) - developed with 6.12.0

### Supported Operating Systems
Currently supported OS are Mac OS, Ubuntu and Windows. You can probably run the project on other OS but you have to install the requirements by yourself. In the documentation there is an installation guide for Mac OS, Ubuntu and Windows.

#### Installation for Windows

You can install Python 3 for Windows from [this link](https://www.python.org/downloads/windows/). At the time of developing the project, the latest Python version is 3.8.2. Keep in mind that if you are using Windows XP or earlier the latest version is Python 3.4.3. 

Depending on your processor type (32-bit or 64-bit) you should install [Windows x86 executable installer](https://www.python.org/ftp/python/3.7.7/python-3.7.7.exe) or [Windows x86-64 executable installer](https://www.python.org/ftp/python/3.7.7/python-3.7.7-amd64.exe). 

Once the download is ready, open the executable file and you will see an installation wizard pop up. You can set your own installation path for Python 3 if you like, but default will do the work for you. In the bottom of the wizard there is are two checkboxes. Make sure "Add Python 3.x to PATH" is selected in order to make the installation process easier. 

If you have installed Python 3 successfully, you should have PIP (Package Installer for Python) installed as well. Check out [this article](https://medium.com/@mahmudahsan/how-to-use-python-pipenv-in-mac-and-windows-1c6dc87b403e) in order to install `pipenv`. `pipenv` is a virtual environment and the idea is that you don't have to install all Python dependencies for the project on your machine and with just 1 simple command you can have them all while you are running the project.

In order to install Node JS for Windows go to [this link](https://nodejs.org/en/download/) and select the Windows installer. Once it is installed you will have to go through the installation wizard. PATH will be set automatically and `npm` will be installed automatically.

#### Installation for Ubuntu

First, you need to have Python 3 on your machine. To install it:

1.  Start by updating the packages list and installing the prerequisites:
    ```
    $ sudo apt update
    ```
2.  Add the deadsnakes PPA to your sources list:
    ```
    $ sudo add-apt-repository ppa:deadsnakes/ppa
    ```
    When prompted press  `Enter`  to continue:
    ```output
    Press [ENTER] to continue or Ctrl-c to cancel adding it.
    ```
3.  Once the repository is enabled, install Python 3.7 with:
    ```
    $ sudo apt install python3.7
    ```
4.  At this point, Python 3.7 is installed on your Ubuntu system and ready to be used. You can verify it by typing:
    ```
    $ python3.7 --version
    ```
Then, you need `pip`:
1.  Use the following command to install pip for Python 3:
    ```
    $ sudo apt install python3-pip
    ```
    The command above will also install all the dependencies required for building Python modules.
    
2.  Once the installation is complete, verify the installation by checking the pip version:
    ```
    $ pip3 --version
    ```

Check out [this article](https://gist.github.com/kogcyc/07c3e5d1f427c9fa6b99044d81f8ee82) for detailed explanation on how to install `pipenv`.

Finally, you need Node JS and `npm`
1. Install Node JS:
    ```
    $ sudo apt install nodejs
    ```
2. You can verify that Node JS was installed by typing:
    ```
    $ nodejs -v
    ``` 
3. In this case, you will need to install `npm` as well:
    ```
    $ sudo apt install npm
    ```
4. Make sure that `npm` is installed successfully by typing:
    ```
    $ npm -v
    ```

#### Installation for Mac OS

To install Python 3 on Mac OS go to [this link](https://www.python.org/downloads/mac-osx/) and choose version to download. You will have to go through a quick setup wizard but then you are good to go.

If you are using Mac OS High Sierra (version 10.13) or newer you can install Python 3 via Homebrew:
```
$ brew install python3
```
If you don't have Homebrew on your Mac, check out [Homebrew's Installation Guide](https://docs.brew.sh/Installation) on how to install Homebrew.

By installing Python 3 you will also have `pip` installed automatically.

Then you need to install `pipenv` which can be installed by:
```
$ brew install pipenv
```
 or
```
$ pip3 install pipenv
```

Finally, you will need to install Node JS and `npm`. Go to [this link](https://nodejs.org/en/download/) and install Node JS for Mac OS. Once installed, open the package and follow the steps in the Node JS Installer. Once you are done, you should have both Node JS and `npm` installed on your Mac.
To verify, you can open Terminal and type the following commands:
```
$ node -v
$ npm -v
```

#### You are now all set! Let's run the project! 

### To Run

Go to Terminal (Mac OS or Ubuntu) or Command Prompt (Windows) and type the following commands:
```
$ cd Odyssey/odyssey
$ make
```
The Makefile runs the following script:
```makefile
all:
    make flask & make svelte
    
flask:
    pipenv install && pipenv run flask run
    
svelte:
    cd client/ && npm install && npm run autobuild
```

### To Edit

Go to Terminal (Mac OS and Ubuntu) or Command Prompt (Windows) and type the following commands:
```
$ cd Odyssey/odyssey
$ pipenv install
$ pipenv shell
$ cd client/
$ npm install
```
`pipenv` will install any libraries used in Flask, whereas `npm` will install any libraries used in Svelte JS.
When you have finished developing, you can exit the virtual environment by typing:
`$ exit` in `/odyssey` directory.

### IDE

We have used [Sublime Text 3](https://www.sublimetext.com/3) for developing the project. You can also install `Svelte` from Package Control for Svelte syntax highlighting


### Braching Strategy

[GitHub Flow](https://githubflow.github.io/)

- Anything in the master branch is deployable
- To work on something new, create a descriptively named branch off of master
- Commit to that branch locally and regularly push your work to the same named branch on the server
- When you need feedback or help, or you think the branch is ready for merging, open a pull request
- After someone else has reviewed and signed off on the feature, you can merge it into master
- Everything branches off of master and merges back to master

### Libraries

[Flask](https://flask.palletsprojects.com/en/1.1.x/) for backend
[Svelte JS](https://svelte.dev/) for frontend and REST API
[Page JS](https://visionmedia.github.io/page.js/) for routing web page
[PyMongo](https://api.mongodb.com/python/current/tutorial.html) as database
[Python Dotenv](https://pypi.org/project/python-dotenv/) for app configurations

### Creators

[Gabriela Yoncheva](https://github.com/GabrielaY) \
[Ognian Baruh](https://github.com/ogi02)

### About

[Official assignment](https://docs.google.com/document/d/1fe4PTeQvuJQCtzLAepiWgYKQRrgO0HffOD3cP5iOwkI/edit?usp=sharing) \
[Additional notes](https://docs.google.com/document/d/1MGU3UjkklhmtIZYOXibMGOLQSNI5sJdpi29l_KBRsfU/edit) \
[Overview](https://docs.google.com/spreadsheets/d/19rgsBmh61TQRARmx8KPktfGFi1IK6kYtLRE6ENJNaMM/edit#gid=0)