import os
import requests

forge_versions = requests.get("https://v1.meta.multimc.org/net.minecraftforge/")

versions_json = forge_versions.json()

versions = []
for version in versions_json["versions"]:
    versions.append(version)


latest_version = versions[0]
latest_version_mc_version = latest_version["requires"][0]["equals"]
latest_version_number = latest_version["version"]

url = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/"+latest_version_mc_version+"-"+latest_version_number+"/forge-"+latest_version_mc_version+"-"+latest_version_number+"-mdk.zip"

project_name = input("Project name\n> ")
os.mkdir(project_name)
os.chdir(project_name)


