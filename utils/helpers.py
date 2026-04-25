import json

# saves json data
def save_json(data: dict, path: str) -> None:
    with open(path, "w") as file:
        json.dump(data, file, indent=2)

# loads json data
def load_json(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)