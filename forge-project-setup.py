import os
import requests
import zipfile
import argparse
from git import Repo
import glob

def setup_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Name of the project to create")
    parser.add_argument("-f", "--forge_version", help="Forge MDK version to download")
    parser.add_argument("-m", "--mc_version", help="Download the latest Forge MDK version which supports this Minecraft version. Ignored when -f is used")
    parser.add_argument("-g", "--create_git_repo", help="Initialise a git repository in the project folder", action="store_true")
    return parser.parse_args()

def get_forge_versions(): 
    forge_versions = requests.get("https://v1.meta.multimc.org/net.minecraftforge/")
    versions_json = forge_versions.json()

    versions = []
    for version in versions_json["versions"]:
        versions.append(version)
    return versions

def download_and_extract_mdk(version):
    version_mc_version = version["requires"][0]["equals"]
    version_number = version["version"]

    url = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/"+version_mc_version+"-"+version_number+"/forge-"+version_mc_version+"-"+version_number+"-mdk.zip"
    download_zip = requests.get(url)

    with open("tmp.zip", 'wb') as fd:
        for chunk in download_zip.iter_content(chunk_size=128):
            fd.write(chunk)

    with zipfile.ZipFile("tmp.zip", 'r') as zip_file:
        zip_file.extractall(".")
        zip_file.close()
    os.remove("tmp.zip")

def create_git_repo():
    assert Repo.init(".").__class__ is Repo

def get_version_to_download(versions, args):
    if (args.forge_version == None):
        if (args.mc_version == None):
            return versions[0]

        for version in versions:
            if (version["requires"][0]["equals"] == args.mc_version):
                return version

    for version in versions:
        if (version["version"] == args.forge_version):
            return version

def delete_unneeded_files():
    for file in glob.glob("./*.txt"):
        os.remove(file)

args = setup_arguments()

versions = get_forge_versions()
version = get_version_to_download(versions, args)

os.mkdir(args.project_name)
os.chdir(args.project_name)

download_and_extract_mdk(version)

if (args.create_git_repo):
    create_git_repo()

delete_unneeded_files()
