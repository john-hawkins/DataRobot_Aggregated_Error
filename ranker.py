import datarobot as dr
import pandas as pd

def generated_aggregated_error_ranking( project, models, col_one, col_two, error_metric, df, max_test):
   results = []
   index = 0
   dataset = project.upload_dataset(df)
   df = change_column_names(df)
   for mod in models:
      result = {}
      result['index'] = index
      result['model_type'] = mod.model_type
      result['sample_pct'] = mod.sample_pct
      result['features'] = mod.featurelist_name
      result['metric'] = mod.metrics[ project.metric ]['validation']
      agg_cols = [col_one, col_two]
      if index<max_test:
          agg = calculate_aggregated_error(project, mod, agg_cols, error_metric, df, dataset)
      else:
          break
      result['AGG'] = round(agg, 2)
      results.append(result)
      index = index+1
   newlist = sorted(results, key=lambda k: k['AGG']) 
   return newlist


############
def change_column_names(df):
    cols = df.columns
    new_names = [ x.replace('.', '_') for x in cols]
    df.columns = new_names   
    return df

# ##########
# THIS VERSION REQUIRES THAT YOU PROVIDE A DATA SET FOR THE AGGREGATION
def calculate_aggregated_error(project, mod, agg_cols, error_metric, df, dataset) :
    predict_job = mod.request_predictions(dataset.id)
    preds = predict_job.get_result_when_complete(max_wait=6000)
    #preds = predictions.get_all_as_dataframe()
    df['prediction'] = preds['prediction']
    preds_col = 'prediction'
    actuals_col = project.target
    print(df.columns)
    print(agg_cols)
    agg_actuals = df.groupby(agg_cols, as_index=False)[[actuals_col]].sum()
    agg_preds = df.groupby(agg_cols, as_index=False)[[preds_col]].sum()
    new_df = pd.merge(agg_actuals, agg_preds, how='left', left_on=agg_cols, right_on = agg_cols )
    agg_errs = new_df[preds_col] - new_df[actuals_col]
    # NOT GUARANTEED
    # agg_pct_err = 100 * (agg_errs/new_df[preds_col])
    # agg_mape = abs(agg_pct_err).mean()
    if error_metric=='MAE':
       return abs(agg_errs).mean()
    else :
       return pow( pow(agg_errs,2).sum(), 0.5)

# 
# THIS VERSION DOES NOT WORK BECAUSE THERE IS NO WAY TO INCLUDE OTHER COLUMNS
# WHEN RETRIEVING THE TRAINING PREDICTIONS
def calculate_aggregated_error_holdout(project, mod, agg_cols, error_metric) :
    preds_col = 'prediction'
    actuals_col = project.target
    if project.partition['cv_method']== 'datetime' :
        # training_predictions_job = mod.request_training_predictions(dr.enums.DATA_SUBSET.ALL_BACKTESTS)
        training_predictions_job = mod.request_training_predictions('allBacktests')
    else :
        training_predictions_job = mod.request_training_predictions(dr.enums.DATA_SUBSET.VALIDATION_AND_HOLDOUT)
    training_predictions = training_predictions_job.get_result_when_complete(max_wait=6000)
    df = training_predictions.get_all_as_dataframe()
    agg_actuals = df.groupby(agg_cols, as_index=False)[[actuals_col]].sum()
    agg_preds = df.groupby(agg_cols, as_index=False)[[preds_col]].sum()
    new_df = pd.merge(agg_actuals, agg_preds, how='left', left_on=agg_cols, right_on = agg_cols )
    agg_errs = new_df[preds_col] - new_df[actuals_col]
    # NOT GUARANTEED
    # agg_pct_err = 100 * (agg_errs/new_df[preds_col])
    # agg_mape = abs(agg_pct_err).mean()
    if error_metric=='MAE':
       return abs(agg_errs).mean()
    else :
       return pow( pow(agg_errs,2).sum(), 0.5)

