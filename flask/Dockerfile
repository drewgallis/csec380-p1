#
# Drew Gallis
# CSEC 380
# Flask Dockerfile Config File
#


FROM python:latest
COPY ./ /app
WORKDIR /app
RUN pip install -r  ./requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
