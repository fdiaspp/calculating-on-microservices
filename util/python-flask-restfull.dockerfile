FROM python:3.7

RUN pip install --no-cache-dir \
        flask \
        flask_restful \
        flask_cors      \
        requests