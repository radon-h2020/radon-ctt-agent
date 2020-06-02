#!/usr/bin/env python

# Native imports
import logging
import os

# Module imports
from flask import Flask
from flask_api import status
from straight.plugin.loaders import ModuleLoader

logging.basicConfig(level=logging.INFO)

base_path = '/tmp/radon-ctt-agent'


def register_plugins(plugin_list):
    for plugin in plugin_list:
        if plugin.storage_enabled:
            plugin_path = os.path.join(base_path, plugin.prefix)
            os.makedirs(plugin_path, exist_ok=True)
            plugin.register(app, plugin_path)
        else:
            plugin.register(app)


app = Flask(__name__)
app.debug = False
plugins = ModuleLoader().load('plugins')
register_plugins(plugins)


@app.route('/')
def index():
    return f'This is the Radon Continuous Testing Tool (CTT) Agent.', status.HTTP_200_OK


if __name__ == '__main__':
    app.run(host='0.0.0.0')
