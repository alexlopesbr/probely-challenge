# Challenge Probely
This project consists of a command that needs to be run to consume data from a given endpoint and store it in the project's database. The solution also provides an endpoint to retrieve the acquired data, with the possibility of filtering it.

> Following good practices, django's secret key was hidden, but displayed here for didactic purposes

    SECRET_KEY = django-insecure-qfiii^8ox@=7-n$dzyoe(e8-#jx_og%ed$5u=*g&8)grw5u)!b

# Instructions
To use this project, follow the steps below:

1. Create and activate a virtual environment:
    ```shell
    python3 -m venv venv
    ```

2. Active it
    ```shell
    source venv/bin/activate
    ```

3. Install the required libraries:
    ```shell
    pip install -r requirements.txt
    ```

4. Run the server
    ```shell
    python manage.py runserver
    ```

5. Run the command with the argument to retrieve the data and store it in the database:
    ```shell
    python manage.py feed_data_with_finds <target_id>
    ```

6. To bring all data just call que endpoint. Replace {definition_id} and {scan} with the desired filter values.

    > http://localhost:8000/findings/?definition_id={definition_id}&scan={scan}

- You can use Insomnia, Postman or terminal to do the request
    ```shell
    curl --request GET \
    --url 'http://127.0.0.1:8000/api/core/findings?scan=236WQ2MH4uKA&definition_id=0fR9GA5lgbo6'
    ```

7. Run the tests
    ```shell
    ./manage.py test
    ```


This project was lovingly developed by Alexandre.

>LinkedIn: https://www.linkedin.com/in/alexandre-backend-python/

>Email: criabiobr@gmail.com

>Phone: +353 0833428700
