from flask import current_app 

def documento_url(documento):
    client = current_app.storage.client

    if documento is None:
        return ""
    

    return client.presing_get_object("grupo49", documento)
