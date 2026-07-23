import json
import os


def load_config():

    path = os.path.join(
        "config",
        "artemis.json"
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)