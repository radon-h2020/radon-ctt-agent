#!/usr/bin/env python

# Native imports
import logging
import os

# Module imports
from flask import Flask
from straight.plugin.loaders import ModuleLoader
from waitress import serve


logging.basicConfig(level=logging.INFO)

base_path = '/opt/radon-ctt-agent'


def register_plugins(plugin_list):
    logging.info(f'Found {len(plugin_list)} plugins.')
    for plugin in plugin_list:
        if plugin.storage_enabled:
            plugin_path = os.path.join(base_path, plugin.prefix)
            os.makedirs(plugin_path, exist_ok=True)
            plugin.register(app, plugin_path)
        else:
            plugin.register(app)

        logging.info(f'> Plugin {plugin} registered')


app = Flask(__name__)
app.debug = False
plugins = ModuleLoader().load('plugins')
register_plugins(plugins)


@app.route('/')
def index():
    return f'This is the Radon Continuous Testing Tool (CTT) Agent.', 200


if __name__ == '__main__':
    serve(app=app, host="0.0.0.0", port=5000)
