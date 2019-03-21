from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from pathlib import Path
import numbers
import pandas as pd
import datarobot as dr
import os

# ranker.py
import ranker as rnk

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ###################################################################################
# Index Page
@app.route('/')
def index():
    # GET THE LIST OF PROJECTS
    projs = dr.Project.list()
    return render_template("index.html", projects=projs)


# ###################################################################################
# Second step 
@app.route('/configure', methods = ['POST', 'GET'])
def configure():
    if request.method == 'POST':
       project_id = request.form["project_id"]
    proj = dr.Project.get(project_id=project_id)
    proj_type = proj.target_type
    mods = proj.get_models()
    useable_mods = filter_out_mods_without_metrics(proj, mods)
    feats = mods[0].get_features_used()   
    projs = dr.Project.list()
    return render_template("configure.html", project=proj, models=useable_mods, projects=projs, features=feats)

# ###################################################################################
def filter_out_mods_without_metrics(project, mods):
    results = []
    for mod in mods:
        if ( isinstance( mod.metrics[project.metric]['validation'], numbers.Number) ): 
            results.append(mod)
    return results
    
# ###################################################################################
# Generate it
@app.route('/rank', methods = ['POST', 'GET'])
def rank():
    if request.method == 'POST':
        project_id = request.form["project_id"]
        col_one = request.form["col_one"]
        col_two = request.form["col_two"]
        error_metric = request.form["error_metric"]
        max_test = int(request.form["max_test"])
        proj = dr.Project.get(project_id=project_id)
        mods = proj.get_models()

        # ########################################################
        if 'file' not in request.files:
            message = 'No file supplied'
            print("Message: ", message)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            message = 'empty filname'
            print("Message: ", message)
        nrows = 0
        ncols = 0
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            pdata = pd.read_csv(filepath, low_memory=False)
            nrows =  len(pdata)
            ncols = len(pdata.columns)

        ranked_leaderboard = rnk.generated_aggregated_error_ranking(project=proj, models=mods, col_one=col_one, col_two=col_two, 
                                                                    error_metric=error_metric, df=pdata, max_test=max_test)

        return render_template("ranked.html", project=proj, error_metric=error_metric,
                               models=ranked_leaderboard)

# ###################################################################################
# About Page
@app.route('/about')
def about():
        return render_template("about.html")


# ###################################################################################
# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)


