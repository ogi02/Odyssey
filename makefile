flask:
	cd odyssey/api/ && pipenv install && pipenv run flask run
	
react:
	cd odyssey/ && npm start

run:
	make flask & make react
