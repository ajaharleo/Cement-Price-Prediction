from flask import Flask, request
import sys
import pip
from CementStrength.utils import *
from matplotlib.style import context
from CementStrength import logger, get_log_dataframe
import os, sys
import json
from pathlib import Path
from CementStrength.config import Configuration
from CementStrength.constants import *
from CementStrength.pipeline import Pipeline
from CementStrength.entity.concrete_predictor import ConcretePredictor, ConcreteData
from flask import send_file, abort, render_template
CONFIG_DIR = os.path.dirname(CONFIG_FILE_PATH)

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "concrete_strength"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


CONCRETE_DATA_KEY = "concrete_data"
CONCRETE_COMPRESSIVE_STRENGTH_KEY = "concrete_compressive_strength"

app = Flask(__name__)


@app.route('/concrete_artifact', defaults={'req_path': 'concrete_artifact'})
@app.route('/concrete_artifact/<path:req_path>')
def render_artifact_dir(req_path):
    try:
        os.makedirs("concrete_artifact", exist_ok=True)
        # Joining the base and the requested path
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            if ".html" in abs_path:
                with open(abs_path, "r", encoding="utf-8") as file:
                    content = ''
                    for line in file.readlines():
                        content = f"{content}{line}"
                    return content
            return send_file(abs_path)

        # Show directory contents
        files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
                "artifact" in os.path.join(abs_path, file_name)}

        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template('files.html', result=result)
    except Exception as e:
        logger.exception(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.exception(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    try:
        experiment_df = Pipeline.get_experiments_status()
        context = {
            "experiment": experiment_df.to_html(classes='table table-striped col-12')
        }
        return render_template('experiment_history.html', context=context)
    except Exception as e:
        logger.exception(e)

@app.route('/train', methods=['GET', 'POST'])
def train():
    try:
        message = ""
        pipeline = Pipeline(config=Configuration(current_time_stamp=get_current_time_stamp()))
        if not Pipeline.experiment.running_status:
            message = "Training started."
            pipeline.start()
        else:
            message = "Training is already in progress."
        context = {
            "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
            "message": message
        }
        return render_template('train.html', context=context)
    except Exception as e:
        logger.exception(e)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        context = {
            CONCRETE_DATA_KEY: None,
            CONCRETE_COMPRESSIVE_STRENGTH_KEY: None
        }

        if request.method == 'POST':
            cement = float(request.form['cement'])
            blast_furnace_slag = float(request.form['blast_furnace_slag'])
            fly_ash = float(request.form['fly_ash'])
            water = float(request.form['water'])
            superplasticizer = float(request.form['superplasticizer'])
            coarse_aggregate = float(request.form['coarse_aggregate'])
            fine_aggregate = float(request.form['fine_aggregate'])
            age = float(request.form['age'])

            concrete_data = ConcreteData(cement=cement,
                                        blast_furnace_slag=blast_furnace_slag,
                                        fly_ash=fly_ash,
                                        water=water,
                                        superplasticizer=superplasticizer,
                                        coarse_aggregate=coarse_aggregate,
                                        fine_aggregate=fine_aggregate,
                                        age=age)
            concrete_df = concrete_data.get_concrete_input_data_frame()
            concrete_predictor = ConcretePredictor(model_dir=MODEL_DIR)
            concrete_compresive_strength = concrete_predictor.predict(X=concrete_df)
            context = {
                CONCRETE_DATA_KEY: concrete_data.get_concrete_data_as_dict(),
                CONCRETE_COMPRESSIVE_STRENGTH_KEY: concrete_compresive_strength,
            }
            return render_template('predict.html', context=context)
        return render_template("predict.html", context=context)
    except Exception as e:
        logger.exception(e)

@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    try:
        os.makedirs("saved_models", exist_ok=True)
        # Joining the base and the requested path
        print(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return send_file(abs_path)

        # Show directory contents
        files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template('saved_models_files.html', result=result)
    except Exception as e:
        logger.exception(e)

@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml(file_path=Path(MODEL_CONFIG_FILE_PATH), data=model_config)

        model_config = read_yaml(path_to_yaml=Path(MODEL_CONFIG_FILE_PATH))
        return render_template('update_model.html', result={"model_config": model_config})

    except Exception as e:
        logger.exception(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    try:
        os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
        # Joining the base and the requested path
        logger.info(f"req_path: {req_path}")
        abs_path = os.path.join(req_path)
        print(abs_path)
        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)
    # Check if path is a file and serve
        if os.path.isfile(abs_path):
            log_df = get_log_dataframe(abs_path)
            context = {"log": log_df.to_html(classes="table-striped", index=False)}
            return render_template('log.html', context=context)

        

        # Show directory contents
        files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

        result = {
            "files": files,
            "parent_folder": os.path.dirname(abs_path),
            "parent_label": abs_path
        }
        return render_template('log_files.html', result=result)
    except Exception as e:
        logger.exception(e)

if __name__ == "__main__":
    app.run()