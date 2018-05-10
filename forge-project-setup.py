import os
import requests
import zipfile
import argparse
from git import Repo
import glob
import shutil

def setup_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Name of the project to create")
    parser.add_argument("-f", "--forge_version", help="Forge MDK version to download")
    parser.add_argument("-m", "--mc_version", help="Download the latest Forge MDK version which supports this Minecraft version. Ignored when -f is used")
    parser.add_argument("-g", "--create_git_repo", help="Initialise a git repository in the project folder", action="store_true")
    parser.add_argument("-r", "--remove_unneeded_files", help="Remove unneeded txt files in project directory", action="store_true")
    parser.add_argument("-p", "--package_name", help="Package name for the mod")
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

    version_greater_than_1_7_0 = int(version_mc_version.split(".")[1]) > 7

    if (version_greater_than_1_7_0):
        url_template = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/{0}-{1}/forge-{0}-{1}-mdk.zip"
    else:
        url_template = "http://files.minecraftforge.net/maven/net/minecraftforge/forge/{0}-{1}/forge-{0}-{1}-src.zip"
    url = url_template.format(version_mc_version, version_number)
    download_zip = requests.get(url)

    with open("tmp.zip", 'wb') as fd:
        for chunk in download_zip.iter_content(chunk_size=128):
            fd.write(chunk)

    with zipfile.ZipFile("tmp.zip", 'r') as zip_file:
        zip_file.extractall(".")
        zip_file.close()
    os.remove("tmp.zip")

    if (not version_greater_than_1_7_0):
        for file in glob.glob("forge/*"):
            shutil.move(file, ".")

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

def rename_package(package_name):
    replace_in_file("com.yourname.modid", package_name, "build.gradle")
    shutil.rmtree("src/main/java/com")
    os.makedirs("src/main/java/"+package_name.replace(".","/"))

def replace_in_file(find, replace, path):
    # Read in the file
    with open(path, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(find, replace)

    # Write the file out again
    with open(path, 'w') as file:
        file.write(filedata)

args = setup_arguments()

versions = get_forge_versions()
version = get_version_to_download(versions, args)

os.mkdir(args.project_name)
os.chdir(args.project_name)

download_and_extract_mdk(version)

if (args.create_git_repo):
    create_git_repo()
if (args.remove_unneeded_files):
    delete_unneeded_files()
if (args.package_name != None):
    rename_package(args.package_name)
