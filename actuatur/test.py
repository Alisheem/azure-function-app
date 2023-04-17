with open("../git.properties", "r") as f:
    properties = {}
    for line in f:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        key, value = line.split("=", 1)
        properties[key] = value

print(properties["git.branch"])