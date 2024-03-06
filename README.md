# Inspire API

### Summary
An application to get local land charge ID by inspire ID. Inspire stands for Index Polygons Spatial Data and is an opensource dataset. For more information, you can check it out here: https://use-land-property-data.service.gov.uk/datasets/inspire
This application is built to run on our common development environment (common dev-env), which you can read more about here: https://github.com/LandRegistry/common-dev-env

### Documentation
The API has been documented using OpenAPI (fka Swagger) YAML files. 
The swagger files can be found under the [documentation](inspire_api/documentation) directory.
At present the documentation is not hooked into any viewer within the dev environment. To edit or view the documentation open the YAML file in swagger.io <http://editor.swagger.io>

### Local Quick Start (Outside Docker)
```shell
# For Flask CLI
export FLASK_APP=inspire_api/main.py
export FLASK_DEBUG=1
# For Python
export PYTHONUNBUFFERED=yes
# For gunicorn
export PORT=8169
# For app's config.py
export FLASK_LOG_LEVEL=DEBUG
export COMMIT=LOCAL
export APP_NAME=inspire-api

# Run the app
flask run
```

### Unit tests

The unit tests are contained in the unit_tests folder. [Pytest](http://docs.pytest.org/en/latest/) is used for unit testing. 

To run the unit tests if you are using the common dev-env use the following command:

```bash
docker-compose exec inspire-api make unittest
or, using the alias
unit-test inspire-api
```

or

```bash
docker-compose exec inspire-api make report="true" unittest
or, using the alias
unit-test inspire-api -r
```

### Linting

Linting is performed with [Flake8](http://flake8.pycqa.org/en/latest/). To run linting:
```bash
docker-compose exec inspire-api make lint
```

## Updating Requirements

To update the requirements for this repo, you can use [pur](https://pypi.org/project/pur/) to find the latest versions for the respective dependencies. To make this happen, change directory (cd) into the desired repo and run each of these commands consecutively:
```
docker run --rm -it -v $PWD:/src python:3.9 bash
cd /src
pip install pip-tools
pip install pur
pur -r requirements.in
pur -r requirements_test.txt
pip-compile
exit
```