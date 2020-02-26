FROM ustctt/ctt-agent:base

WORKDIR /opt

ENV JMETER_VERSION 5.2.1
ENV JMETER_NAME apache-jmeter-$JMETER_VERSION
ENV JMETER_BIN_URL http://ftp.halifax.rwth-aachen.de/apache/jmeter/binaries/$JMETER_NAME.zip
ENV JMETER_TMP_DL_PATH /tmp/jmeter.tgz

RUN apk add openjdk11-jre-headless

RUN wget -q $JMETER_BIN_URL -O $JMETER_TMP_DL_PATH &&\
    unzip -q $JMETER_TMP_DL_PATH -d /opt 
ENV PATH="/opt/$JMETER_NAME/bin:$PATH"
