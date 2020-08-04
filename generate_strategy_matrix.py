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


def fetch_releases(token, owner, name, last_n:int):
    releases = []
    data = client.execute(
        query=make_query(owner, name, 100),
        headers={"Authorization": "Bearer {}".format(token)},
    )
    for release in reversed(data["data"]["repository"]["releases"]["nodes"]):
        tag_name = release["tagName"]
        if tag_name.split(".")[-1].isnumeric():
            releases.append(tag_name[1:] if tag_name[0] == "v" else tag_name)
        if len(releases) == last_n:
            break
    return releases


def strategy_matrix(token, owner, name, last_n:int, python_versions, tag_latest=True):
    repo_versions = fetch_releases(token=token, owner=owner, name=name, last_n=last_n)
    repo_name_for_matrix = f"{args.name.upper()}_VERSION"
    matrix = {
        "include": [
            {repo_name_for_matrix: repo_version, "PYTHON_VERSION": python_version,
            "TAGS":f"{python_version}-{repo_version}"}
            for python_version in python_versions
            for repo_version in repo_versions
        ]
    }
    if tag_latest:
        matrix["include"][0]["TAGS"] += ",latest"
    return matrix


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--owner", help="owner of the repo", type=str, required=True,
    )
    parser.add_argument(
        "--name", help="name of the repo", type=str, required=True,
    )
    parser.add_argument(
        "--last_n", help="the last n releases", type=int, required=True,
    )
    parser.add_argument(
        "--token", help="Github personal access token", type=str, required=True,
    )
    
    args = parser.parse_args()
    
    pythons = [3.8, 3.7, 3.6]

    matrix = strategy_matrix(python_versions=pythons, **vars(args))
    print(json.dumps(matrix))

    

