FROM alpine:latest

WORKDIR /opt

EXPOSE 5000
HEALTHCHECK --start-period=10s CMD curl --fail "http://localhost:5000/" || exit 1

ENV PATH="/root/.local/bin:$PATH"

RUN apk update && apk upgrade && apk add curl python3 py3-pip
RUN pip3 install --no-cache --upgrade pip
RUN pip3 install --user --no-cache virtualenv

ENTRYPOINT ["run_ctt_agent.sh"]
