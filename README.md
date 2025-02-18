# Fake review detector


Fake review detector has both the training script and the website.

## Installation

First, you need to have [Python](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/) installed on your system.

### Training script

First, cd into ```training_script``` directory.

#### Windows/Linux
```bash
cd training_script
```
Then create a poetry shell and install all dependencies

#### Windows/Linux
```bash
poetry shell
poetry install
```

Then use find the virtual environment path and use it as the Python interpreter in your IDE of choice:

#### Windows/Linux
```bash
poetry env info --path # Then copy the output for virtual environment path
```

From this point you can open the file ```fake-review-detector.ipynb``` and execute the cells to execute the training script.

### Website (recommened)

First, cd into ```fake-review-detector-api``` directory.

#### Windows
```bash
cd fake-review-detector-api
```

Then create a poetry shell and install all dependencies

#### Windows/Linux
```bash
poetry shell
poetry install
```

In the ```.env``` file, the ```API_KEY``` environment variable will already have the API key needed for the website to accept requests at the endpoint, /detect/. However, for the ```READ_TOKEN``` you will need to provide your own token. This can be generated by making an account on [Huggingface](https://hf.co) and then going to settings and access tokens, there you can generate read tokens.

Once the your own read token has been assigned to ```READ_TOKEN``` in the ```.env``` file, you can run the server inside a poetry shell.

#### Windows
```bash
poetry run py .\manage.py runserver
```

#### Linux/Unix
```bash
poetry run python3 manage.py runserver
```

The server will run on localhost and on port 8000, you can click this [link](http://localhost:8000) to access it.

### Website via Docker

If you are having trouble with install the packages, you can instead use docker. First you will need to install both Docker Desktop and Docker Compose via this [link](https://docs.docker.com/compose/install/). 

In the ```.env``` file, the ```API_KEY``` environment variable will already have the API key needed for the website to accept requests at the endpoint, /detect/. However, for the ```READ_TOKEN``` you will need to provide your own token. This can be generated by making an account on [Huggingface](https://hf.co) and then going to settings and access tokens, there you can generate read tokens.

You will then need to cd into ```fake-review-detector-api``` directory.
#### Windows/Linux
```bash
cd fake-review-detector-api
```

Once installed, you will need to first have Docker Desktop open and then build the image.

#### Windows
```bash
docker build -t fake-review-detector .    
```

Then, once the image has been created, you can run the container.

#### Windows
```bash
docker run -it -p 8000:8000 fake-review-detector
```
The server will run on localhost and on port 8000, you can click this [link](http://localhost:8000) to access it.

## Usage

The website has an API at the endpoint /detect/, this endpoint takes POST requests and needs the review to be loaded into the body of the request as a JSON with the form, {"inputs": "<review>"}. In addition, the header of the request needs "Authorization: Api-Key <```API_KEY``` in the ```.env``` file>".

This can even be done by a cURL request.
#### Linux/Unix
```bash
curl http://localhost:8000/detect/ -X POST -d '{"inputs": "Hello, world?"}' -H "Authorization: Api-Key <API_KEY>" -H "Content-Type: application/json"
```

You can also just write whatever you want into the form on the website and it returns the deceptiveness/truthfulness.