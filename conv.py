import json
import gzip
import time

def convert():
    with open("discoveries.json", "r") as f:
        data = json.load(f)

    output = {
        "name": "My Save",
        "version": "1.0",
        "created": int(time.time() * 1000),
        "updated": 0,
        "instances": [],
        "items": [
            {"id": i, "text": item["name"], "emoji": item["emoji"]}
            for i, item in enumerate(data)
        ]
    }

    with open("output.ic", "wb") as f:
        f.write(gzip.compress(json.dumps(output).encode()))

    print("Done! Upload output.ic to the game.")


