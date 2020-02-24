#!/usr/bin/env python

# Native imports
import datetime
import logging
import os
import shutil
import tempfile
import uuid

# Module imports
from flask import Flask, jsonify, request, send_file
# from flask_plugins import PluginManager
from flask_api import status



from setuptools import setup, find_namespace_packages

app = Flask(__name__)
app.debug = False
# plugin_manager = PluginManager(app)
# plugin_list = plugin_manager.all_plugins()

persistence = {
    "jmeter": {
        "configuration": {},
        "execution": {},
    },
    "ab": {
        "configuration": {},
        "execution": {},
    },
    "locust": {
        "configuration": {},
        "execution": {},
    },
    'qt': {
        "configuration": {},
        "execution": {},
    }
}


# zip
# - config
# - execution

storage_path = '/tmp/UST-CTT-Agent'
jmeter_executable = '/usr/bin/env jmeter'

test_plan_filename = 'test_plan.jmx'
test_properties_filename = "jmeter.properties"
test_run_log_filename = 'run.log'
test_results_dashboard_folder_name = 'dashboard'
test_sample_results_filename = 'sample_results.jtl'

# Folder in local storage where configuration artifacts are stored
# (e.g., <storage_path>/<config_uuid>/<storage_config_folder_name/)
storage_config_folder_name = 'config'

result_zip_file_name = 'results.zip'

# Names of the folders in the results zip file
result_config_folder_name = 'config'
result_execution_folder_name = 'execution'


@app.route('/')
def index():
    return f'This is the Radon Continuous Testing Tool (CTT) Agent.', status.HTTP_200_OK


############# JMETER #############

# Create Configuration
@app.route('/jmeter/configuration/', methods=['POST'])
def jmeter_configuration_create():
    config_instance = {}

    configuration_uuid = str(uuid.uuid4())
    config_instance['uuid'] = configuration_uuid

    config_path_relative = os.path.join(configuration_uuid, storage_config_folder_name)
    config_path = os.path.join(storage_path, config_path_relative)
    os.makedirs(config_path, exist_ok=True)

    # Test plan (file)
    test_plan_path = None
    if 'test_plan' in request.files:
        test_plan = request.files['test_plan']
        test_plan_path = os.path.join(config_path, test_plan_filename)
        test_plan.save(test_plan_path)
        config_instance['test_plan_path'] = \
            os.path.join(config_path_relative, test_plan_filename)
    else:
        return 'No test plan provided.', status.HTTP_400_BAD_REQUEST

    # Properties file
    if 'properties' in request.files:
        properties = request.files['properties']
        properties_path = os.path.join(config_path, test_properties_filename)
        properties.save(properties_path)
        config_instance['properties_path'] = \
            os.path.join(config_path_relative, test_properties_filename)

    persistence['jmeter']['configuration'][configuration_uuid] = config_instance

    return_json = {
        'configuration': {
            'uuid': configuration_uuid,
            'entry': config_instance
        }
    }
    return jsonify(return_json), status.HTTP_201_CREATED


# Get/Delete Configuration
@app.route('/jmeter/configuration/<string:config_uuid>/', methods=['GET', 'DELETE'])
def jmeter_configuration_getdelete(config_uuid):
    if config_uuid in persistence['jmeter']['configuration']:
        if request.method == 'GET':
            return_json = {
                'configuration': {
                    'uuid': config_uuid,
                    'entry': persistence['jmeter']['configuration'][config_uuid]
                }
            }
            return jsonify(return_json), status.HTTP_200_OK

        if request.method == 'DELETE':
            del persistence['jmeter']['configuration'][config_uuid]
            shutil.rmtree(os.path.join(storage_path, config_uuid))
            return 'Successfully deleted ' + config_uuid + '.', status.HTTP_200_OK

    else:
        return "No configuration with that ID found", status.HTTP_404_NOT_FOUND


# Run load test (param: configuration uuid)
@app.route('/jmeter/loadtest/', methods=['POST'])
def jmeter_loadtest_execute():
    execution_instance = {}

    if 'config_uuid' in request.form:
        config_uuid = request.form['config_uuid']
        config_entry = persistence['jmeter']['configuration'][config_uuid]
        execution_instance['config'] = config_entry

        # Create UUID for execution
        execution_uuid = str(uuid.uuid4())
        execution_instance['uuid'] = execution_uuid

        # Execution folder will be below configuration folder
        execution_path = os.path.join(storage_path, config_uuid, execution_uuid)

        jmeter_cli_call = [jmeter_executable]
        jmeter_cli_call.append('-n')  # cli mode (mandatory)
        jmeter_cli_call.append('-e')  # generate report dashboard
        jmeter_cli_call.append('-o ' + os.path.join(execution_path,
                                                    test_results_dashboard_folder_name))  # output folder for report dashboard
        jmeter_cli_call.append('-j ' + os.path.join(execution_path, test_run_log_filename))
        jmeter_cli_call.append('-l ' + os.path.join(execution_path, test_sample_results_filename))

        # Possible extensions
        # * -r -R remote (server mode)
        # * -H -P Proxy
        # * many more ( jmeter -? )
        # * Parameter string for -Dpropkey=propvalue

        if 'test_plan_path' in config_entry:
            os.mkdir(execution_path)
            jmeter_cli_call.append('-t ' + os.path.join(storage_path, config_entry['test_plan_path']))

            if 'properties_path' in config_entry:
                jmeter_cli_call.append('-p ' + os.path.join(config_entry['properties_path']))

        else:
            return "Configuration does not contain a test plan.", status.HTTP_404_NOT_FOUND

        execution_instance['cli_call'] = jmeter_cli_call

        logging.info("JMeter CLI call: ", jmeter_cli_call)

        execution_start = datetime.datetime.now()
        os.system(' '.join(jmeter_cli_call))
        execution_end = datetime.datetime.now()

        execution_instance['execution_start'] = execution_start
        execution_instance['execution_end'] = execution_end

        with tempfile.NamedTemporaryFile() as tf:
            tmp_zip_file = shutil.make_archive(tf.name, 'zip', execution_path)
            shutil.copy2(tmp_zip_file, os.path.join(execution_path, result_zip_file_name))

        persistence['jmeter']['execution'][execution_uuid] = execution_instance

        return jsonify(execution_instance), status.HTTP_200_OK

    else:
        return "No configuration with that ID found.", jsonify(persistence), status.HTTP_404_NOT_FOUND


# Get load test results
@app.route('/jmeter/loadtest/<string:exec_uuid>/', methods=['GET'])
def jmeter_loadtest_results(exec_uuid):
    try:
        config_uuid = persistence.get('jmeter').get('execution').get(exec_uuid).get('config').get('uuid')
    except AttributeError:
        return "No execution found with that ID.", status.HTTP_404_NOT_FOUND

    results_zip_path = os.path.join(storage_path, config_uuid, exec_uuid, result_zip_file_name)
    if os.path.isfile(results_zip_path):
        return send_file(results_zip_path)
    else:
        return "No results available (yet).", status.HTTP_404_NOT_FOUND


if __name__ == '__main__':
    app.run(host='0.0.0.0')
