# adapted from https://github.com/simonw/simonw/blob/main/build_readme.py
import argparse
from python_graphql_client import GraphqlClient
import json
import pathlib
import re
import os

root = pathlib.Path(__file__).parent.resolve()
client = GraphqlClient(endpoint="https://api.github.com/graphql")


TOKEN = os.environ.get("SIMONW_TOKEN", "")


def make_query(owner, name, last_n):
    return (
        """
query { 
  repository(owner:"$OWNER", name: "$NAME") { 
    releases(last: $LAST_N){
      nodes{
        tagName
      }
    }
  }
}
""".replace(
            "$OWNER", owner
        )
        .replace("$NAME", name)
        .replace("$LAST_N", str(last_n))
    )


def fetch_releases(oauth_token, owner, name, last_n):
    releases = []
    data = client.execute(
        query=make_query(owner, name, 100),
        headers={"Authorization": "Bearer {}".format(oauth_token)},
    )
    for release in reversed(data["data"]["repository"]["releases"]["nodes"]):
        tag_name = release["tagName"]
        if tag_name.split(".")[-1].isnumeric():
            releases.append(tag_name[1:] if tag_name[0] == "v" else tag_name)
        if len(releases) == last_n:
            break
    return releases


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token", help="Githun personal access token", type=str, default=None,
    )

    args = parser.parse_args()
    pipenvs = fetch_releases(args.token, "pypa", "pipenv", 5)
    pythons = [3.8, 3.7, 3.6]
    matrix = {
        "include": [
            {"PIPENV_VERSION": pipenv_version, "PYTHON_VERSION": python_version}
            for python_version in pythons
            for pipenv_version in pipenvs
        ]
    }
    print(json.dumps(matrix))

