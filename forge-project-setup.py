import os
import requests

forge_versions = requests.get("https://v1.meta.multimc.org/net.minecraftforge/")

versions_json = forge_versions.json()

version_numbers = []
for version in versions_json["versions"]:
    version_numbers.append(version["version"])

print(version_numbers)
project_name = input("Project name\n> ")
os.mkdir(project_name)
os.chdir(project_name)


