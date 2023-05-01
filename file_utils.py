def save_locally(data, uploaded_file):
    import os.path
    import pathlib
    import os
    from azure.storage.blob import BlobServiceClient
    import requests
    session = requests.session()
    session.verify = False

    parent_path = pathlib.Path(__file__).parent.resolve()           
    save_path = os.path.join(parent_path, "data")
    complete_name = os.path.join(save_path, uploaded_file.name)
    destination_file = open(complete_name, "w")
    destination_file.write(data)
    destination_file.close()

    # Save to Azure and get uri for blob
    upload_file_path = os.path.join('./data', uploaded_file.name)
    local_file_name = uploaded_file.name
    container_name = 'chatgpt-csv-reader-blob'

    blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=chatgptcsvreadersa;AccountKey=g6dNIAzHoig03KUGSwOXQgMaCrQkmLEqdLegxWQL8vX5gVgcRPztcbMSD8EtnOLY98YSPs22/LyS+AStrhdaug==;EndpointSuffix=core.windows.net', session=session)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    container_client = blob_service_client.get_container_client(container=container_name)

    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)
        file_uri = blob_client.url

    blob_list = container_client.list_blobs()

    for blob in blob_list:
        print(f"Name: {blob.name} ")
    
    return file_uri


