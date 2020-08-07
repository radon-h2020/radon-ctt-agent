FROM alpine:latest

WORKDIR /opt

EXPOSE 5000
HEALTHCHECK --start-period=10s CMD curl --fail "http://localhost:5000/" || exit 1


# Name of the folder inside the downloaded ZIP-file
ENV AGENT_DIR "/opt/radon-ctt-agent"
ENV PLUGIN_DIR "$AGENT_DIR/plugins"
ENV PATH="$AGENT_DIR:/root/.local/bin:$PATH"

RUN apk update && apk upgrade && apk add curl python3 py3-pip
RUN pip3 install --no-cache --upgrade pip
RUN pip3 install --user --no-cache virtualenv

RUN mkdir -p "$PLUGIN_DIR"
COPY ctt-agent.py run_ctt_agent.sh requirements.txt "${AGENT_DIR}/"

ENTRYPOINT ["run_ctt_agent.sh"]
