# Resume_Parser Using Natural Language Processing (Python)
This is small resume parser project, It is rest service that can be used to parse resume.
It is created using :- 
1.) flask
2.) nltk
- Directory Structure
	RAS_SERVICE
		|__app
		|   |__main
		|	|__model (includes all database models)
		|	|
		|	|__controller (include all controller function)
		|	|
		|	|__service (include service code for each controller function)
		|	|
		|	|__util (include dto (data transfer object)
		|	|
		|	|
		|	|__config.py (configuration file)
		|	|
		|	|__ __init__.py 
		|   |__test
		|	|__ __init__.py 
		|   |__ __init__.py 
		|__manage.py  (file for running the service)
		|
		|
		|__path_and_url.py (file includes all configurations, path, urls)
		|
		|__requirements.txt (includes all dependencies required to run service
		|
		|__README.md

- running service

	1.) python3 manage.py run

- References
https://www.omkarpathak.in/2018/12/18/writing-your-own-resume-parser/


