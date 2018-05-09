# forge-project-setup
An application to automate creation of new forge projects.

Automatically downloads and extracts the mdk, and optionally:
 - removes the unnecessary txt files
 - adds your package name to build.gradle
 - initialises a git repo

Does not work for minecraft versions < 1.7.10.

```ShellSession
usage: forge-project-setup.py [-h] [-f FORGE_VERSION] [-m MC_VERSION] [-g]
                              [-r] [-p PACKAGE_NAME]
                              project_name

positional arguments:
  project_name          Name of the project to create

optional arguments:
  -h, --help            show this help message and exit
  -f FORGE_VERSION, --forge_version FORGE_VERSION
                        Forge MDK version to download
  -m MC_VERSION, --mc_version MC_VERSION
                        Download the latest Forge MDK version which supports
                        this Minecraft version. Ignored when -f is used
  -g, --create_git_repo
                        Initialise a git repository in the project folder
  -r, --remove_unneeded_files
                        Remove unneeded txt files in project directory
  -p PACKAGE_NAME, --package_name PACKAGE_NAME
                        Package name for the mod
```
