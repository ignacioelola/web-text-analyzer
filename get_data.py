#!/usr/bin/env python
# Description: Script to get MPs financial interests
__author__ = 'ignacioelola'

import csv
import requests
import json
import time
import importio_rsc


def get_web_data(guid, url):

    query = {"input": {"webpage/url": url}}
    response = importio_rsc.query_api(query, guid)
    data = response["results"][0].get("blob")

    return data


def data_analyzer(text, source):
    data = {
        'text_list': [text]
    }

    response = requests.post(
        "https://api.monkeylearn.com/v2/extractors/ex_y7BPYzNG/extract/",
        data=json.dumps(data),
        headers={'Authorization': 'Token YOUR-TOKEN',
                'Content-Type': 'application/json'})

    results = json.loads(response.text)["result"][0]
    analysis = []
    for result in results:
        row = {"relevance": result.get("relevance"),
               "keyword": result.get("keyword"),
               "source": source,
               "datetime": time.strftime("%Y-%m-%d %H:%M:%S")}
        analysis.append(row)
    return analysis


def data_savior(data, filename):
    with open(filename, "a") as outfile:
        writer = csv.writer(outfile)
        for record in data:
            row = []
            if "source" in record:
                row.append(record["source"])
            else:
                row.append("")
            if "datetime" in record:
                row.append(record["datetime"])
            else:
                row.append("")
            if "keyword" in record:
                row.append(record["keyword"])
            else:
                row.append("")
            if "relevance" in record:
                row.append(record["relevance"])
            else:
                row.append("")
            writer.writerow(row)



if __name__ == '__main__':

    sources = {"The Guardian UK Politics": {"guid": "7787398d-af1a-438f-9d0d-06521069c2cf",
                                "source_url": "http://www.theguardian.com/politics"},
               "The Telegraph UK Politics": {"guid": "3338f0f3-21c7-4b40-809b-a37440dc8e12",
                                "source_url": "http://www.telegraph.co.uk/news/politics/"},
               }

    filename_output = "data/output.csv"

    # Extract data
    for source in sources:
        text = get_web_data(sources[source]["guid"], sources[source]["source_url"])
        analysis = data_analyzer(text, source)
        data_savior(analysis, filename_output)
