#
# THIS SCRIPT SHOW YOU HOW TO GENERATE THE AGGREGATED ERROR RANKED LIST
# WITHOUT USING THE WEB APPLICATION
#
# IT PRESUMES THAT YOU HAVE A YAML CONFIG FILE TO AUTHENTICATE AGAINST
# DataRobot

import datarobot as dr
import pandas as pd

# ranker.py
import ranker as rnk

path_to_file = ""
project_id = ""

col_one = "Name of first column to aggregate over"
col_two = "Name of second column to aggregate over"
error_metric = "MAE"
max_test = 5 

proj = dr.Project.get(project_id=project_id)
mods = proj.get_models()

pdata = pd.read_csv(filepath, low_memory=False)

ranked_leaderboard = rnk.generated_aggregated_error_ranking(project=proj, models=mods, col_one=col_one, col_two=col_two,
                                                                    error_metric=error_metric, df=pdata, max_test=max_test)

print(ranked_leaderboard)


