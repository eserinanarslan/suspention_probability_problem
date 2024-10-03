import pandas as pd
import os
import sqlite3 as sql
import flask
from flask import request, jsonify
import configparser
import json
import warnings
import logging
from datetime import datetime

# Ignore warnings
warnings.filterwarnings("ignore")
pd.set_option('display.float_format', '{:.4f}'.format)

# Ensure the logs directory exists
log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Initialize logging
log_filename = os.path.join(log_dir, f'service_log_{datetime.now().strftime("%Y-%m-%d")}.log')
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logging.info("Starting the service and loading configuration.")

# Read the config.ini file
config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

# Log config file reading
logging.info("Loaded configuration file: config.ini")

# Construct the correct relative path to the database
db_path = os.path.join(os.getcwd(), 'data', 'results.db')

# Connect to the SQLite database
try:
    conn = sql.connect(db_path)
    print(f"Successfully connected to the database at: {db_path}")
    data = pd.read_sql("SELECT * FROM suspention_results", conn).drop(columns="index")
    logging.info("Data loaded from SQLite database.")
except Exception as e:
    print(f"Failed to connect to the database. Error: {e}")
    logging.error(f"Error loading data: {e}")
    raise


# Function to format columns
def column_format(data):
    try:
        data['random_for_probability'] = data['random_for_probability'].apply(lambda x: '{:.3f}'.format(x))
        data['naive_bias_probability'] = data['naive_bias_probability'].apply(lambda x: '{:.3f}'.format(x))
        data['cal_naive_bias_probability'] = data['cal_naive_bias_probability'].apply(lambda x: '{:.3f}'.format(x))
        data['Suspention_Score'] = data['Suspention_Score'].apply(lambda x: '{:.2f}'.format(x))
        logging.info("Column formatting applied successfully.")
        return data
    except Exception as e:
        logging.error(f"Error during column formatting: {e}")
        raise

# Apply column formatting
data = column_format(data)

# Convert data to JSON
try:
    df = data.to_json(orient="records")
    df = json.loads(df)
    logging.info("Data successfully converted to JSON.")
except Exception as e:
    logging.error(f"Error converting data to JSON: {e}")
    raise

# Initialize Flask app
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/get_all_results', methods=['GET'])
def total_api():
    try:
        logging.info("GET request received at /get_all_results")
        return jsonify(df[:100])
    except Exception as e:
        logging.error(f"Error in /get_all_results: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/search_user_result', methods=['GET'])
def api_id():
    try:
        logging.info("GET request received at /search_user_result")
        # Check if user_id is provided
        if 'user_id' in request.args:
            user_id = request.args['user_id']
            logging.info(f"User ID: {user_id} requested.")
        else:
            logging.warning("No user_id provided in request.")
            return "Error: No user_id field provided. Please specify an user id.", 400

        # Find matching results
        results = [record for record in df if record["user_id"] == user_id]

        # Return results or 404 if no matches
        if len(results) < 1:
            logging.info(f"user_id {user_id} not found.")
            return "userId is not found", 404
        else:
            logging.info(f"user_id {user_id} found.")
            return jsonify(results)
    except Exception as e:
        logging.error(f"Error in /search_user_result: {e}")
        return jsonify({"error": str(e)}), 500

# Start the Flask app
try:
    logging.info("Starting the Flask server.")
    app.run(host=config["Service"]["Host"], port=int(config["Service"]["Port"]), debug=True)
except Exception as e:
    logging.error(f"Error starting the Flask server: {e}")
