import logging
import os
import openai
import json
import ssl
import warnings
import certifi
certifi.where()
# from urllib3.exceptions import InsecureRequestWarning

# ssl._create_default_https_context = ssl._create_unverified_context

# from contextlib import contextmanager

# @contextmanager
# def no_ssl_verification():
#     # Suppress SSL warnings
#     with warnings.catch_warnings():
#         warnings.simplefilter("ignore", InsecureRequestWarning)
#         yield

current_directory = os.path.abspath(os.getcwd())
os.environ['REQUESTS_CA_BUNDLE'] = f'{current_directory}/Baltimore CyberTrust Root.crt'

def OpenAiApiRequest(prompt:str, bot_role:str, data: str):
    try:
        logging.info('Function processed a request.')

        if not data:
            logging.info(f"Missing parameter 'data':{data}")
            raise Exception(f"Missing paramater 'prompt':{data}")
        else:
            if not prompt:
                logging.info(f"Missing paramater 'prompt':{prompt}")
                raise Exception(f"Missing paramater 'prompt':{prompt}")

        # Load your API key from an environment variable or secret management service
        openai.api_type = "azure"
        openai.base_url = os.getenv("AZURE_OPENAI_API_BASE")
        openai.api_version = "2023-09-15-preview"
        openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        # openai.azure_endpoint = os.getenv("AZURE_ENDPOINT")

        openai_req = [{"role":"system","content":f"{bot_role}"},{"role":"user","content":f"{prompt}\\n\\n{data}"}]

        # with no_ssl_verification():
        #     # Make a request to the API
        #     response = openai.ChatCompletion.create(
        #         engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), 
        #         messages = openai_req,
        #         temperature=0.7,
        #         # model="gpt-35-turbo",
        #         max_tokens=500,
        #         top_p=0.95,
        #         frequency_penalty=0,
        #         presence_penalty=0,
        #         stop=None
        #     )
        # Make a request to the API
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), 
            messages = openai_req,
            temperature=0.7,
            max_tokens=500,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        logging.info(f"This function returned result {response.choices[0].message.content}")
        summary = json.loads('{"summary":"' + response.choices[0].message.content + '"}')
        return summary
    except Exception as e:
        logging.error(f"An exception occurred: {e}")
        strerror = '{"error" :"' + f"An exception occurred: {e}"+ '"}'
        return json.loads(strerror)
