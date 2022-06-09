FROM python:3.10-slim

WORKDIR /app/

ARG UID
ARG GID
RUN groupadd --gid ${GID} newuser
RUN useradd --uid ${UID} --gid ${GID} --create-home --shell /bin/bash newuser
RUN chown ${UID}:${GID} /app/
USER newuser

COPY app/ .
COPY src/unexpected_isaves src/unexpected_isaves
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
