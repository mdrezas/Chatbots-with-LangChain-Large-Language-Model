# Ultima-2 🌱

# OpenAI API Key:
https://openai.com/blog/openai-api

# ActiveLoop API Token:
https://www.activeloop.ai

# Please update the following credentials in utils.py as needed
activeloop_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
activeloop_org_name = 'XXXXXXXX'

# Create virtual environment
python -m venv /path/to/new/virtual/environment

# To install required files
pip install -r requirements.txt

# To run this pall run the following command 
streamlit run app.py

# To run this with files more then 200MB run following command 
streamlit run app.py --server.maxUploadSize=500

# Please adjust the follwing parameters in shared_attribs.py as needed
k, k_fetch, max_token, chunk_size, chunk_overlap, and temparature

# For UML Diagram 
pip install pylint
pip install graphviz

# Run
pyreverse ultima -o png