import os.path
import pathlib
from azure.storage.blob import BlobServiceClient
import os
import openai

def save_locally(data,uploaded_file):
    parent_path = pathlib.Path(__file__).parent.resolve()           
    save_path = os.path.join(parent_path, "data")
    complete_name = os.path.join(save_path, uploaded_file.name)
    destination_file = open(complete_name, "w")
    destination_file.write(data)
    destination_file.close()


    # Save to Azure and get uri for blob
    local_file_name = uploaded_file.name
    upload_file_path = os.path.join('./data', uploaded_file.name)
    container_name = 'chatgpt-csv-blob-container'

    blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=chatgpt1storage1account;AccountKey=7QEs3/6esMQiV4XDActHuT19waXVyuIOWwh+7ioFVjP29btO0qdIC+xoEY7Hp28b+/YLzkY3JclI+AStOB9kHQ==;EndpointSuffix=core.windows.net')
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    container_client = blob_service_client.get_container_client(container=container_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    try:
        with open(file=upload_file_path, mode="rb") as data:
            blob_client.upload_blob(data)
            file_uri = blob_client.url
            blob_client.delete_blob()
    except:
        pass

    return file_uri
    
def query_openai(file_uri):
    openai.api_key = "9a47e79663cf450197049f1c2cbb5371"#os.getenv("OPENAI_API_KEY")
    openai.api_base = "https://openai-cog-pcginfra-1rhut0vngi9-sbx.openai.azure.com/" #os.getenv("OPENAI_API_ENDPOINT") # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    openai.api_type = 'azure'
    openai.api_version = '2022-12-01' # this may change in the future
    deployment_name="OpenAi-Test-text-davinci-003"

    response = openai.Completion.create(
    engine=deployment_name,  
    model="text-davinci-003",
    prompt="What is this data about "+file_uri,
    temperature=0,
    max_tokens=150,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )
    output = response["choices"][0]["text"]
    return output  
