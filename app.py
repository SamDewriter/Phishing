"""Smart Phishing Detection System using Machine Learning and Streamlit"""

import base64
import copy
import pickle

import pandas as pd
import streamlit as st
import toml
import validators

from utils.extractor import FeaturesExtractor

# Load the model
config = toml.load('config.toml')
# Columns to be used for training
columns = config["training"]["columns"]

pickle_path = config["pickle"]["file_path"]
with open(pickle_path, 'rb') as f:
    model = pickle.load(f)

def is_single_column(file_path):
    """Check if the uploaded CSV file has just one column."""
    try:
        df = pd.read_csv(file_path) # pylint: disable=invalid-name
        # if df.shape[1] == 1:
        #     return False
        return df.shape[1] == 1 and len(df.columns) > 0
    except pd.errors.ParserError:
        return False
    # except pd.errors.EmptyDataError:
    #     return False

# def is_valid_url(url): # pylint: disable=R1710
#     """Check if the URL is valid."""
#     try:
#         if validators.url(url):
#             return True
#     except validators.ValidationFailure:
#         return False

def predict_single_url(url):
    """
    Predict if the URL is a phishing URL or not.
    
    Args:
        url (str): The URL to be checked.
    Returns:
        pred (int): The prediction result.    
    """
    features = FeaturesExtractor(url).all_features()
    df = pd.DataFrame([features], columns=columns) # pylint: disable=C0103
    pred = model.predict(df)

    return pred

def predict_multiple_urls(df: pd.DataFrame): # pylint: disable=C0103
    """
    Predict if the URLs are phishing URLs or not.

    Args:
        df (pd.DataFrame): The DataFrame containing the URLs.
    Returns:
        pred_df (pd.DataFrame): The DataFrame containing the URLs and the predictions.
    """
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
    """Main function of the app."""
    st.title('Smart Phishing Detection System')
    st.image('phishing.jpg', width=700)

    st.sidebar.header('User Input Features')
    st.sidebar.write("""Please provide the following information to
                     check if the website is a phishing website or not.""")

    st.sidebar.header('Single URL Check')
    url = st.sidebar.text_input('Enter the URL here:')
    button = st.sidebar.button('Submit')

    st.sidebar.header('Multiple URL Check')
    st.sidebar.write('Please upload a CSV file with just one column:')
    st.sidebar.write('- URL(s)')
    uploaded_file = st.sidebar.file_uploader('Upload your CSV file here.', type=['csv'])

    if button:
        if url:
            st.write('---')
            st.write('The URL you entered is:')
            st.write(url)

            prediction = predict_single_url(url)

            if prediction[0] == 0:
                st.write('This is a legitimate URL.')
            elif prediction[0] == 1:
                st.write('This is a phishing URL.')
        else:
            st.sidebar.error("""
                Error: The URL you entered is not valid.
                Please enter a valid URL.""")

    else:
        if uploaded_file is not None:

            check_file = copy.copy(uploaded_file)
            if is_single_column(check_file):
                df = pd.read_csv(uploaded_file) # pylint: disable=C0103
                st.write("CSV file uploaded successfully")

                st.write('---')
                st.write('The URLs:')
                st.write(df.head(10))

                load_df = predict_multiple_urls(df)
                # Load the predictions
                st.write('---')
                st.write('Multiple Prediction Results')
                st.dataframe(load_df)

                st.write('---')
                # Do basic analysis on the predictions
                st.subheader('Basic Analysis on the Prediction Results')
                st.write('Total number of URLs:', load_df.shape[0])
                st.write('Total number of Legitimate URLs:',
                         load_df["Prediction"].value_counts()[0])
                st.write('Total number of Phishing URLs:',
                         load_df["Prediction"].value_counts()[1])


                # Download the predictions
                st.write('---')
                st.write('Download the prediction results here:')
                csv = load_df.to_csv(index=False)

                # some strings <-> bytes conversions necessary here
                b64 = base64.b64encode(csv.encode()).decode()
                href = f"""<a href="data:file/csv;base64,{b64}"
                                    download="prediction.csv">Download CSV File</a>"""
                st.markdown(href, unsafe_allow_html=True)

            else:
                st.sidebar.error("""
                    Error: The uploaded CSV File has more than one column.
                    Upload a CSV file with just one column.""")

                # else:
                #     st.error("Error: The uploaded CSV file has more than one column")

if __name__ == '__main__':
    main()
