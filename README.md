
Aggregated Error
========================

This project allows you to connect to DataRobot and re-rank the leaderboard by looking at the 
aggregated error of a selection of the top models.

You will need a data set to use to calculate the aggregated error.

This data set should be relatively small (on the order of megabytes) so that you can get results in a reasonable time.

## Dependencies
 
You will need a DataRobot account and access to a dedicated prediction server.

You will also need a bunch of python libraries, including the DataRobot API

```
pip install numpy
pip install pandas
pip install datarobot
```

The application presumes you have YAML file set up to authenticate you against the DataRobot sever.


## About

In certain machine learning scenarios the impact of the model error on a business process
does not happen at the level of individual predictions. Instead the aggregation of predictions
across key subsets determines how the business process is affected.

This means that model selection should take into consideration the error of these aggregated predictions.


## Usage

If you want to use the functionality within a script then the file [Example.py](Example.py) will show you how.

The file [app.py](app.py) and the contents of the [templates](templates) directory is a python flask 
web application you can use to select a DataRobot project, and then the column you want to use to 
perform the aggregation.


To run:

```
python app.py
```

Then follow the prompts



