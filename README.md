# RADON Continuous Testing Tool (CTT) Agent

Test Execution Agent for the Radon Continuous Testing Tool (CTT)

[![Build Status](https://travis-ci.com/UST-CTT/radon-ctt-agent.svg?branch=master)](https://travis-ci.com/UST-CTT/radon-ctt-agent)

| Items | Contents |
| --- | --- |
| **Description** | The Continuous Testing Tool Agent provides the basic framework to be extended by [testing tool plugins](https://github.com/radon-h2020/radon-ctt-agent-plugins) providing the funcitonality for specific testing tools. |
| **Licence**| Apache License, Version 2.0: https://opensource.org/licenses/Apache-2.0 |
| **Maintainers**| <ul><li>Thomas F. Düllmann ([@duelle](https://github.com/duelle)) </li><li>Andre van Hoorn ([@avanhoorn](https://github.com/avanhoorn)) </li></ul> |

## System Requirements

This README is currently tailored to Unix-like systems (Linux, MacOS).

For CTT users, the following software must be installed:

1. Python3
1. Python Virtual Environment (`virtualenv`)

For CTT developers, the following additional software must be installed:
1. Docker
1. Recommended: A Python IDE such as [PyCharm](https://www.jetbrains.com/pycharm/)

## Starting the CTT Agent

The CTT Agent is not supposed to be used standalone but deployed and controlled by the CTT Server. For testing and development purposes, it is possible to start it manually, either as a Docker container or directly on the local machine.

### Using Docker

1. Run the following command to pull and run the CTT Agent JMeter container: `docker run -tdi --rm --name radon-ctt-agent-jmeter -p 5000:5000 ustctt/ctt-agent:jmeter`
1. The API of the CTT Agent is now available with the URL base: `http://localhost:5000/`


### Local machine

Execute the following steps to start start and access the CTT Agent:

1. Clone this repository (if not done, yet)
1. Start the CTT server by executing  `./run_ctt_agent.sh`
1. Access the CTT server's API using the following URL base: `http://localhost:5000/`


## Developing/Extending the CTT Agent

1. When using an IDE: import the CTT Server Agent repository into your IDE

