#!/usr/bin/env python
# description: Resources to use the importio platform
__author__ = 'ignacioelola'

import requests
import json
import time
import urllib
import sys
import os
import inspect


# Function to read your credentials.
# Credentials need to be in a JSON file called auth_credentials.json
#  in the format:
# {
# "userGuid": YOUR-USER-GUID,
# "apiKey": YOUR-API-KEY
# }
def read_credentials():
    with open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/auth_credentials.json",
              "r") as infile:
        auth_credentials = json.load(infile)
    return auth_credentials


# Function to paginate through a URL
def paginate_url(url, page):

    paginated_url = url + str(page)

    return paginated_url


# Function to query the REST API
def query_api(query,
              api_guid,
              page=None,
              endpoint="http://api.import.io/store/connector/"):

    auth_credentials = read_credentials()

    timeout = 5

    if page is not None and "webpage/url" in query["input"]:
        paginated_url = paginate_url(query["input"]["webpage/url"], page)
        query["input"]["webpage/url"] = paginated_url

    try:
        r = requests.post(
            endpoint + api_guid + "/_query?_user=" + auth_credentials["userGuid"] + "&_apikey=" + urllib.quote_plus(
                auth_credentials["apiKey"]),
            data=json.dumps(query), timeout=timeout)
        rok = r.ok
        rstatus_code = r.status_code
        rtext = r.text
    except:
        rok = False
        rstatus_code = 000
        rtext = "exception"

    if rok is True and rstatus_code == 200 and "errorType" not in r.json():
        results = r.json()
        return results
    else:
        print "Error %s, %s on page %s , Retrying now (1)..." % (rstatus_code, rtext, query["input"]["webpage/url"])
        sys.stdout.flush()
        time.sleep(2.5)

        try:
            r = requests.post(
                endpoint + api_guid + "/_query?_user=" + auth_credentials["userGuid"] + "&_apikey=" + urllib.quote_plus(
                    auth_credentials["apiKey"]),
                data=json.dumps(query), timeout=timeout)
            rok = r.ok
            rstatus_code = r.status_code
            rtext = r.text

        except:
            rok = False
            rstatus_code = 000
            rtext = "exception"

        if rok is True and rstatus_code == 200 and "errorType" not in r.json():
            results = r.json()
            return results
        else:
            print "Error %s, %s on page %s , Could not complete the query" % (rstatus_code, rtext, query["input"]["webpage/url"])
            sys.stdout.flush()
            try:
                error = json.loads(r.content)["error"]
            except:
                try:
                    error = r.status_code
                except:
                    error = "0"
            return error