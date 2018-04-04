import os
import requests
import zipfile

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

download_zip = requests.get(url)

with open("tmp.zip", 'wb') as fd:
    for chunk in download_zip.iter_content(chunk_size=128):
        fd.write(chunk)

with zipfile.ZipFile("tmp.zip", 'r') as zip_file:
    zip_file.extractall(".")
    zip_file.close()
