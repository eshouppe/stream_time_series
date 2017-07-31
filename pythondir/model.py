"""
Get docs for training date range & put into single df
Pivot by date index and quadclass column with counts

Pick AR, I, and MA params

Train model on sample
Save fitted model params as Mongo doc
Use learned model to make in-sample predictions for training period
Save predicted values to docs

Forecast values for the next month
Rinse & repeat
"""
import datetime

import pandas as pd
from pymongo import MongoClient
from statsmodels.tsa.arima_model import ARIMA


def get_docs_from_db(start_date, end_date):
    """
    Connect to MongoDB, make query, and put results in pandas df
    """
    events_cllctn = GDELT_DB.gdeltevents

    get_data_qry = {"eventDate": {"$gte": start_date, "$lte": end_date}}
    get_data_prj = {"eventDate": 1, "quadclass": 1}

    # Create dataframe with requested docs
    docs_df = pd.DataFrame(list(events_cllctn.find(get_data_qry, get_data_prj)))
    return docs_df


def save_model_to_db(model_params, model_type, train_start, train_end):
    """
    Add doc to models collection with learned model params
    """
    model_cllctn = GDELT_DB.models
    param_doc = {
        "model_type": model_type,
        "created_on": datetime.datetime.today(),
        "train_range_start": train_start,
        "train_range_end": train_end
    }
    for idx, val in model_params.iteritems():
        new_idx = idx.replace('.', '_')
        param_doc[new_idx] = val

    insert_result = model_cllctn.insert_one(param_doc)
    if insert_result.acknowledged is False:
        print("Error inserting model params doc in db")


def update_docs_with_prediction(trends_df):
    """
    Would be an update on mapreduced docs. Here is an
    insert since multiple docs exist per day in events data.
    """
    trends_cllctn = GDELT_DB.trends
    for row in trends_df.itertuples():
        trends_doc = {
            "date": row.Index,
            "actual": row.Actual,
            "prediction": row.Predict
        }
        insert_result = trends_cllctn.insert_one(trends_doc)
        if insert_result.acknowledged is False:
            print("Error inserting trends doc in db")


def insert_forecast_docs(predict_vals, last_train_date):
    """
    When model is training with this month's data, we forecast the next
    month's event counts. Save those predictions as new trends docs.
    """
    trends_cllctn = GDELT_DB.trends
    for val in predict_vals:
        last_train_date += datetime.timedelta(days=1)
        predict_doc = {
            "date": last_train_date,
            "prediction": val
        }
        insert_result = trends_cllctn.insert_one(predict_doc)
        if insert_result.acknowledged is False:
            print("Error inserting forecasted trends doc in db")


def train_arima_model(start_dt, end_dt, predict_len):
    """
    Transform data to required format. Fit ARIMA model.
    Good model has small AIC/BIC and large log likelihood.
    """
    raw_train_df = get_docs_from_db(start_dt, end_dt)

    train_df = pd.pivot_table(raw_train_df,
                              values="_id",
                              index="eventDate",
                              columns="quadclass",
                              aggfunc='count',
                              fill_value=0)
    train_df.rename(columns={1:"QC1", 2:"QC2", 3:"QC3", 4:"QC4"}, inplace=True)
    train_df['Actual'] = train_df.sum(axis=1).astype(float)

    model = ARIMA(train_df['Actual'], order=(1, 0, 1),
                  freq='D').fit(trend='c', disp=0)

    save_model_to_db(model.params, 'arima', start_dt, end_dt)

    train_df['Predict'] = model.predict()
    update_docs_with_prediction(train_df[['Actual', 'Predict']])

    next_months_forecast = model.forecast(steps=predict_len)[0]
    insert_forecast_docs(next_months_forecast, end_dt)


if __name__ == "__main__":
    CLIENT = MongoClient('mongodb://localhost:27017/')
    GDELT_DB = CLIENT.gdelt

    train_arima_model(datetime.datetime(2017, 1, 1),
                      datetime.datetime(2017, 1, 31),
                      28)
