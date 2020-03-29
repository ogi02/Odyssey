##  Conventions for Flask

### Requirements for imports
Order of imports:
 1. Built-in imports
 2. Third party library imports
 3. Imports from .py file
 4. Blueprint imports (only in `main.py`) 

Example:
```python
# Built-in imports
import json

# Third party library imports
from flask import Flask, jsonify, request

# Imports from .py files
from user import User

# Blueprint imports (only in main.py)
from profile import profile_bp
```

### Requirements for functions

Please leave comments if there are any tricky parts in the function. Usually python functions are small and their names explain their functionality well enough, so in most cases there won't be any need for explaining the functionality of a function.

Example:
```python
def register_user():
	# explain tricky part 1
	... some code

	# explain tricky part 2
	... some other code	
```

> **Note:** Adding few new lines will make the code easier for reading and understanding. 
