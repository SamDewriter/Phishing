import streamlit as st
import pandas as pd
import pickle
import validators
import copy
import toml
import base64
from urllib.parse import urlparse, parse_qs
from utils.extractor import FeaturesExtractor


# Load the model
config = toml.load('config.toml')
# Columns to be used for training
columns = config["training"]["columns"]

pickle_path = config["pickle"]["file_path"]
with open(pickle_path, 'rb') as f:
    model = pickle.load(f)

def is_single_column(file_path):
    try:
        df = pd.read_csv(file_path)
        # if df.shape[1] == 1:
        #     return False
        return df.shape[1] == 1 and len(df.columns) > 0
    except pd.errors.ParserError:
        return False
    # except pd.errors.EmptyDataError:
    #     return False
    
def is_valid_url(url):
    try:
        if validators.url(url):
            return True
    except validators.ValidationFailure:
        return False

def train_single(url):
    features = FeaturesExtractor(url).all_features()

    df = pd.DataFrame([features], columns=columns)

    pred = model.predict(df)

    return pred

def train_multiple(df: pd.DataFrame):

    pred_df = df.copy()
    features = []
    for url in df["URLs"]:
        feature_extracted = FeaturesExtractor(url).all_features()
        features.append(feature_extracted)

    new_df = pd.DataFrame(features, columns=columns)

    pred = model.predict(new_df)

    pred_df["Prediction"] = pred

    return pred_df
    
def main():
    st.title('Smart Phishing Detection System')
    st.image('phishing.jpg', width=700)

    st.sidebar.header('User Input Features')
    st.sidebar.write('Please provide the following information to check if the website is a phishing website or not.')

    st.sidebar.header('Single URL Check')
    url = st.sidebar.text_input('Enter the URL here:')
    button = st.sidebar.button('Submit')

    st.sidebar.header('Multiple URL Check')
    st.sidebar.write('Please upload a CSV file with just one column:')
    st.sidebar.write('- URL(s)')
    uploaded_file = st.sidebar.file_uploader('Upload your CSV file here.', type=['csv'])

    if button:
        if url:
            if is_valid_url(url):
                st.write('---')
                st.write('The URL you entered is:')
                st.write(url)

                prediction = train_single(url)

                if prediction[0] == 0:
                    st.write('This is a legitimate URL.')
                else:
                    st.write('This is a phishing URL.')
            else:
                st.sidebar.error("""
                    Error: The URL you entered is not valid.
                    Please enter a valid URL.""")

    else:
        if uploaded_file is not None:

            check_file = copy.copy(uploaded_file)
            if is_single_column(check_file):
                df = pd.read_csv(uploaded_file)
                st.write("CSV file uploaded successfully")

                st.write('---')
                st.write('The URLs:')
                st.write(df.head(10))

                load_df = train_multiple(df)
                # Load the predictions
                st.write('---')
                st.write('Multiple Prediction Results')
                st.dataframe(load_df)

                st.write('---')
                # Do basic analysis on the predictions
                st.subheader('Basic Analysis on the Prediction Results')
                st.write('Total number of URLs:', load_df.shape[0])
                st.write('Total number of Legitimate URLs:', load_df["Prediction"].value_counts()[0])
                st.write('Total number of Phishing URLs:', load_df["Prediction"].value_counts()[1])


                # Download the predictions
                st.write('---')
                st.write('Download the prediction results here:')
                csv = load_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)
                # st.write(load_df.to_csv(index=False), encoding='utf-8', header=True)


            else:
                # if is_single_column(uploaded_file) is False:
                    # st.error("Error: The uploaded file is not compatible.")                    
                st.sidebar.error("""
                    Error: The uploaded CSV File has more than one column.
                    Upload a CSV file with just one column.""")

                # else:
                #     st.error("Error: The uploaded CSV file has more than one column")
            
if __name__ == '__main__':
    main()