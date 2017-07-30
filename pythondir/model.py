"""
Train arima model
Get docs for date range (all January)
Put into single df
Pivot by date index and quadclass column with counts

Pick AR, I, and MA params

Train model on sample
Save fitted model params as Mongo doc
Use learned model to make in-sample predictions for January
Save predicted values to docs

Use learned model to make out-of-sample predictions for February
Save predicted values to docs

Update model using February data
Rinse & repeat
"""
import datetime

import matplotlib.pyplot as plt
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


def save_model_to_db(model_params, model_type):
    """
    Add doc to models collection with learned model params
    """
    model_cllctn = GDELT_DB.models
    param_doc = {
        "model_type": model_type,
    }
    for idx, val in model_params.iteritems():
        new_idx = idx.replace('.', '_')
        param_doc[new_idx] = val

    insert_result = model_cllctn.insert_one(param_doc)
    if insert_result.acknowledged == False:
      print("Error inserted model params doc in db")


def update_docs_with_prediction():
    """
    stub
    """
    events_cllctn = GDELT_DB.gdeltevents


def train_arima_model(raw_train_df):
    """
    Transform data to required format. Fit ARIMA model.
    Good model has small AIC/BIC and large log likelihood.
    """
    train_df = pd.pivot_table(raw_train_df,
                              values="_id",
                              index="eventDate",
                              columns="quadclass",
                              aggfunc='count',
                              fill_value=0)
    train_df.rename(columns={1:"QC1", 2:"QC2", 3:"QC3", 4:"QC4"}, inplace=True)
    train_df['All'] = train_df.sum(axis=1).astype(float)

    model = ARIMA(train_df['All'], order=(1, 0, 1),
                  freq='D').fit(trend='c', disp=0)

    save_model_to_db(model.params, 'arima')

    train_df['Predict'] = model.predict()

    # Plot in-sample prediction vs actual
    train_df.All.plot()
    train_df.Predict.plot()
    plt.show()

#
if __name__ == "__main__":
    CLIENT = MongoClient('mongodb://localhost:27017/')
    GDELT_DB = CLIENT.gdelt

    jan_qry_start_dt = datetime.datetime(2017, 1, 1)
    jan_qry_end_dt = datetime.datetime(2017, 1, 31)
    jan_df = get_docs_from_db(jan_qry_start_dt, jan_qry_end_dt)
    train_arima_model(jan_df)
