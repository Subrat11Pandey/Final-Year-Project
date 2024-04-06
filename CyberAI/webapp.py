from re import DEBUG ,sub
from flask import Flask, render_template , request , redirect, send_file , url_for, Response
from werkzeug.utils import secure_filename , send_from_directory
import os , subprocess
from subprocess import Popen
import re , requests ,shutil , time , glob
from PIL import Image
import csv
import firebase_admin

app = Flask(__name__  )
app.config['STATIC_FOLDER'] = 'static'
@app.route('/', methods=['GET', 'POST'])




def index():
    urls_data = read_last_10_urls()
    if request.method == 'POST':
        # Handle form submission
        u_input = request.form['user_input']
        print(u_input)
        # check the input url
        result = check_url(u_input)
        urls_data = read_last_10_urls()
        print(result)
        # update the status to the last 10 checked urls
        # update_url()

    return render_template('index.html',urls_data=urls_data)
def check_url(input_url):
    report ="random description of the text"
    status =  "PASS"
    output = [input_url , report, status]
    # output in the form of array [input_url , report , status]
    # have to post the report to the webpage
    # save_to_db(output)
    save_to_csv(output)

    return output

def read_last_10_urls():
    file_path = 'data.csv'
    urls = []

    try:
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)
            rows = list(csvreader)[-10:]
            for row in reversed(rows):
                urls.append({'url': row[0], 'description': row[1], 'status': row[2]})
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    
    return urls


def save_to_csv(data):
    file_path = 'data.csv'

    # Check if CSV file exists; if not, create a new file and write header
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['URL', 'Description', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if file is newly created
        if not file_exists:
            writer.writeheader()

        # Write data to CSV file
        writer.writerow({'URL': data[0], 'Description': data[1], 'Status': data[2]})
if __name__ == '__main__':
    app.run(debug=True)