#!/usr/bin/env python
__author__ = 'ignacioelola'

import csv
import requests
import json
import time
import sys
import importio_rsc


def get_web_data(guid, url):

    query = {"input": {"webpage/url": url}}
    response = importio_rsc.query_api(query, guid)
    data = response["results"][0].get("text")

    return data


def data_analyzer(text, source):
    data = {
        'text_list': [text],
        'max_keywords': 25,
        'use_company_names': 1,
        'expand_acronyms': 1

    }

    response = requests.post(
        "https://api.monkeylearn.com/v2/extractors/ex_eV2dppYE/extract/",
        data=json.dumps(data),
        headers={'Authorization': 'Token ' + str(sys.argv[1]),
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
                row.append(record["source"].encode("utf-8"))
            else:
                row.append("")
            if "datetime" in record:
                row.append(record["datetime"].encode("utf-8"))
            else:
                row.append("")
            if "keyword" in record:
                row.append(record["keyword"].encode("utf-8"))
            else:
                row.append("")
            if "relevance" in record:
                row.append(record["relevance"].encode("utf-8"))
            else:
                row.append("")
            writer.writerow(row)



if __name__ == '__main__':

    sources = {"El Pais": {"guid": "2d62f5a4-18d3-4fba-bac7-ba75e084b392",
                                "source_url": "http://politica.elpais.com/"},
                "El Mundo": {"guid": "39dfd0c6-fe9a-43d8-8eeb-146f7007a873",
                                "source_url": "http://www.elmundo.es/espana.html?cid=MENUHOM24801"},
                "ABC": {"guid": "117d0acd-b808-45c9-8862-904321f90145",
                                "source_url": "http://m.abc.es/espana.html"},
                "La Razon": {"guid": "04a9c37a-1520-41ea-a664-9972648035fe",
                                "source_url": "http://www.larazon.es/espana"},
                "El Diario": {"guid": "d651cf34-7de7-4728-9db7-678e234a472a",
                                "source_url": "http://www.eldiario.es/politica/"},
               }

    filename_output = "data/output_spain.csv"

    # Extract data
    for source in sources:
        text = get_web_data(sources[source]["guid"], sources[source]["source_url"])
        analysis = data_analyzer(text, source)
        data_savior(analysis, filename_output)
