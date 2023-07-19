# import os
# from deta import Deta

# # Install scikit-learn using pip
# os.system('pip install scikit-learn')

# # Import scikit-learn and get its version
# import sklearn

# # Initialize Deta
# deta = Deta(project_key="a0bNXd677pSL_yb7WpMHmCU7WMDvjKjwCdVhWsipbfTkU", project_id="a04gGuPmbps5")

# sklearn_path = sklearn.__file__
# # Create a new drive client
# drive = deta.Drive("new_drive")

# # Upload scikit-learn library to Deta Drive
# with open(sklearn_path, 'rb') as file:
#     sklearn_content = file.read()

# filename = "scikit-learn.tar.gz"

# # # drive.upload(filename=filename, path=sklearn_path)

# drive.put( 
#           data=sklearn_content)

# # # a0bNXd677pSL_yb7WpMHmCU7WMDvjKjwCdVhWsipbfTkU
# # # a04gGuPmbps5