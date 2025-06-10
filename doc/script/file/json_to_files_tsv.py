#! /usr/bin/env python

import json
import sys

headers = [
    "file_id",
    "file_name",
    "file_size",
    "data_type",
    "data_category",
    "data_format",
    "experimental_strategy",
    "platform",
    "access",
    "case_id",
    "project_id",
]

def comp(j):
    r = []
    for k in headers[0:-2]:
        r.append(str(j.get(k, "")))
    return r

def main(json_filename):
    with open(json_filename, "r") as f:
        jsn = json.load(f)

    print('\t'.join(headers))
    for j in jsn:
        for c in j.get("cases", []):
            r = comp(j)
            r.append(c.get("case_id", ""))
            r.append(c.get("project", {}).get("project_id", ""))
            print('\t'.join(r))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 json_to_files_tsv.py <input_json_file>")
        sys.exit(1)
    main(sys.argv[1])
