import json
import os

import requests

def replace_values(payload, **kwargs):
    """ Adjusts post request by parameters """
    payload['form'].update(kwargs)
    return payload

def convert_payload(payload):
    """ Converts payload to website format (looks like Get) """
    converted = ""
    for k, v in payload['form'].items():
        converted = converted + "&" + str(k) + "=" + str(v)
    return converted

def request_website(**kwargs):
    """ The actual requesting """
    # Read json
    with open(os.path.dirname(os.path.realpath(__file__)) + "/params.json") as json_file:
        payload = json.load(json_file)

    # Replace
    payload = replace_values(payload, **kwargs)

    # Convert
    payload = convert_payload(payload)

    # Put request
    response = requests.post('https://www.brutto-netto-rechner.info/',
                             data=payload,
                             headers={"Content-Type": "application/x-www-form-urlencoded",
                                      "User-Agent": "Chrome/5.0 (Windows NT 8.0; Win32; x32; rv:10.0) Gecko/20100101 Firefox/50.0",
                                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
                                      )

    if response.status_code == 200:
        return response.content
    else:
        raise RuntimeError("Could not connect to website")

if __name__ == "__main__":
    print(request_website())
