FROM alpine:latest

WORKDIR /opt

EXPOSE 5000
HEALTHCHECK --start-period=10s CMD curl --fail "http://localhost:5000/" || exit 1

ENV CTT_AGENT_URL https://github.com/radon-h2020/radon-ctt-agent/archive/master.zip
ENV CTT_AGENT_NAME radon-ctt-agent

RUN apk update && apk upgrade
RUN apk add curl python3 py3-pip
RUN pip3 install --no-cache --upgrade pip
RUN pip3 install --no-cache virtualenv

RUN wget -q $CTT_AGENT_URL -O /tmp/$CTT_AGENT_NAME.zip &&\
    unzip -q /tmp/$CTT_AGENT_NAME.zip -d /opt
ENV PATH="/opt/$CTT_AGENT_NAME:$PATH"

ENTRYPOINT ["run_ctt_agent.sh"]
