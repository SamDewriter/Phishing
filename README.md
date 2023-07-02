# Smart Phishing Detection System

What is Phishing?

Phishing refers to a malicious attempt to deceive individuals or organizations into revealing sensitive information, such as usernames, passwords, credit card details, or other personal or financial data. It is typically carried out by posing as a trustworthy entity or institution, such as a reputable company, bank, or government agency.

Phishing attacks often occur through various communication channels, including emails, text messages (SMS), phone calls, or instant messages. The attackers aim to trick unsuspecting users into clicking on fraudulent links, downloading malicious attachments, or providing confidential information.

This project is built with machine learning to detect malicious/phishing url. 

# Getting Started

## Front End

To use the front-end of the detection system, visit:

https://url-phishing.streamlit.app/

- There is a field on the front-end where you can enter the url you want to check whether it is a phishing url or not. After entering the url, click submit, the machine learning model will process the url and tell whether it is phishing or not. 

- You can also upload a csv file that contain only one column (the URLs that you want to check whether they are phishing or not). After the submission, you will see a table and a basic analysis of the predictions. The predictions can also be downloaded as a csv file

### Things to note
- The front-end won't allow you to upload a CSV file that has more than one column
- The column in the CSV file must have the title <b>URLs</b>
- The input field only takes a valid URL and won't work if given an invalid URL. A valid URL is the one that has all of the components of a URL, namely:
    - A scheme
    - A host
    - A path
    - A query string (Read more: https://www.ibm.com/docs/en/cics-ts/5.2?topic=concepts-components-url)

To run and peek into the code or run the server locally, proceed to the next step (Optional)
 
## Set up dev environment

1. Install Python (3.10.6), if not already installed, and also an IDE of your choice.
2. Clone this report your local machine using the terminal:
    Run `git clone https://github.com/SamDewriter/Phishing.git`
3. Install the requirements (make sure you have the latest version of pip installed) by running the command:
    `pip install -r requirements.txt`
4. Run the local server: `streamlit run app.py`.