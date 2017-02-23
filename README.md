# Zeus - Backend Part of Quint

## Installation

1. Ensure you have virtualenv for Python 2.7
2. Clone the repo
3. Ensure you have MongoDB installed.
4. Ensure you have Redis installed
5. Go into virtualenv environment
6. Run `pip install -r requirements.txt` in the root directory
7. Test that everything is working properly using `python app_test.py`
8. If everything is working, you can start the server using the following steps:
    - `export FLASK_APP=app.py`
    - `flask run`

# Run with Docker (Compose)
1. Change **.env** HOST config to `0.0.0.0`
1. Change **.env** DB_HOST config to `db`
2. `docker-compose up`
