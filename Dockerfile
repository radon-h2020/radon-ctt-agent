FROM alpine:latest

WORKDIR /opt

EXPOSE 5000
HEALTHCHECK --start-period=10s CMD curl --fail "http://localhost:5000/" || exit 1


# Name of the folder inside the downloaded ZIP-file
ENV WORK_DIR_PATH "radon-ctt-agent"

ENV PATH="/opt/$WORK_DIR_PATH:/root/.local/bin:$PATH"

RUN apk update && apk upgrade && apk add curl python3 py3-pip
RUN pip3 install --no-cache --upgrade pip
RUN pip3 install --user --no-cache virtualenv

COPY plugins ctt-agent.py run_ctt_agent.sh requirements.txt "${WORK_DIR_PATH}/"

ENTRYPOINT ["run_ctt_agent.sh"]
