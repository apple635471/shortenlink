FROM python:3.10

RUN mkdir /workspace
WORKDIR /workspace
RUN pip install --upgrade pip

COPY requirements.txt /workspace/

RUN pip install -r requirements.txt
COPY . /workspace/

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["tail -f /dev/null"]

