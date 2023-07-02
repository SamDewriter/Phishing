import streamlit as st
import pandas as pd
import pickle
import validators
import copy
from urllib.parse import urlparse, parse_qs


# Load the model
model = pickle.load(open('model_small.pkl', 'rb'))

def extract_features(url):
    parsed_url = urlparse(url)

    # Extract query params
    query_length = len(parse_qs(parsed_url.query))

    # Extract domain
    domain_tokens = parsed_url.netloc.split(".")
    domain_token_count = len(domain_tokens)

    return [query_length, domain_token_count]

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
    features = extract_features(url)
    df = pd.DataFrame([features], columns=['Querylength', 'domain_token_count'])

    pred = model.predict(df)
    return pred


def train_multiple(df: pd.DataFrame):

    input_df = df.copy()
    features = []
    for url in df["URLs"]:
        feature_extracted = extract_features(url)
        features.append(feature_extracted)

    new_df = pd.DataFrame(features, columns=["Querylength", "domain_token_count"])

    pred = model.predict(new_df)

    input_df["Prediction"] = pred

    return input_df
    
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
                st.write(load_df)

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