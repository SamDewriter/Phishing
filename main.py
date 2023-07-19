from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
# Import utils from the root folder
# import sys
# import os
# from deta import Deta
# sys.path.append("../utils")
from utils.extractor import FeaturesExtractor
import toml
import joblib
import uvicorn

# Load scikit-learn from Deta Drive
# deta = Deta(project_key="a0bNXd677pSL_msuF5hkq9FgXCZx8BV9QKEQaR2QhzSDT")
# db = deta.Base("my_db")
# db.get("scikit-learn")
# sys.path.append("my_db/scikit-learn")

# os.system("tar -xvf my_db/scikit-learn/scikit-learn.tar.gz")

# Load the model
config = toml.load('config.toml')
# Columns to be used for training
columns = config["training"]["columns"]
model = joblib.load('model.pkl')


class URLInput(BaseModel):
    url: str

class MultipleURLInput(BaseModel):
    urls: list

app = FastAPI()

@app.post("/predict")
async def predict(input: URLInput):
    url = input.url

    # Load the pretrained model

    # Extract the features
    features = FeaturesExtractor(url).all_features()
    df = pd.DataFrame([features], columns=columns) # pylint: disable=C0103
    pred = model.predict(df)

    if pred == 1:
        return {"prediction": "Phishing URL"}
    else:
        return {"prediction": "Legitimate URL"}
    

@app.post("/predict_multiple")
async def predict_multiple_urls(input: MultipleURLInput): # pylint: disable=C0103
    """
    Predict if the URLs are phishing URLs or not.

    Args:
        urls (list): The list of URLs to be checked.
    Returns:
        pred (list): The prediction results.
    """
    urls = input.urls
    features = []
    for url in urls:
        features.append(FeaturesExtractor(url).all_features())

    df = pd.DataFrame(features, columns=columns) # pylint: disable=C0103
    pred = model.predict(df)

    return {"prediction": pred.tolist()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
