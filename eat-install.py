import sys

if sys.version_info.major == 1:  # if running python 1, do nothing
    exit()
import sys as c
import os as posix_tools
import argparse
from colorama import *
from requests import get
import zipfile, tarfile
import yaml  # PyYAML module, used for parsing YAML manifests.
import shutil
import glob
import distro


class NotCompatibleWithPython2Error(Exception):
    pass


class UnsupportedPython3VersionError(Exception):
    pass


def download(url, file_name):
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)


UserHome = posix_tools.path.expanduser("~")

parser = argparse.ArgumentParser(prog="Eat Utilities", usage="eatinst target [options]")

parser.add_argument("target", type=str, help="package to install")

parser.add_argument("--system", action="store_true", help="install for all users")

parser.add_argument(
    "--config",
    type=str,
    default=f"{UserHome}/eatconfig.yaml",
    help="configuration file to use (in YAML format)",
)
if not posix_tools.path.isfile(f"{UserHome}/eatconfig.yaml"):
    with open(f"{UserHome}/eatconfig.yaml", "a") as file:
        file.write(
            """# To the extent possible under law, the author(s) have dedicated all copyright and related and
# neighboring rights to this software to the public domain worldwide. This software is distributed
# without any warranty.

# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.\n"""
        )  # THIS LICENSE DOES NOT APPLY TO EAT
        file.write("# This YAML config file contains info on what settings for\n")
        file.write(
            "# Eat to use. You can update this file if you want to personalize\n"
        )
        file.write("# your eat experience.\n")
        file.write("\n")
        file.write("# Block closed-source software from being installed.\n")
        file.write("disallowed_licenses:\n")
        file.write("   - _CLOSED # _ means a value that is not an SPDX identifier\n")
        file.write(
            "# I recommend keeping updates on for security reasons. Uncomment\n# the below if you need silent\n#update checking disabled.\n"
        )
        file.write("#updates_disabled: true\n")
args = parser.parse_args()
gi = args.system
config = yaml.full_load(open(args.config, "r").read())

# Do not run eat if the current Python version causes SyntaxErrors or if the version does not support the current python version
# (highest is probably 3.8)
if c.version_info.major == 2:
    raise NotCompatibleWithPython2Error(
        "eat must be run on python 3+, you are using python 2, UPGRADE YOUR PYTHON FOR SECURITY."
    )
elif c.version_info == 3 and c.version_info.minor < 8:
    raise UnsupportedPython3VersionError(
        "eat must be run on python 3.8 or newer, upgrade your python"
    )
if not posix_tools.path.isdir(f"{UserHome}/eat_sources"):
    print("Need to collect sources to install any app. Collecting sources...")
    posix_tools.system(
        "git clone https://github.com/EatInstall/Network ~/eat_sources --depth 1 >> /dev/null"
    )
elif not config["updates_disabled"]:
    try:
        print("Checking for eat updates...")
        posix_tools.system(
            f"git clone https://github.com/EatInstall/Eat {UserHome}/comparison_eat_both --depth 1"
        )
        for i in glob.glob(f"{UserHome}/Eat-PKG-Manager/*"):
            if posix_tools.path.isfile(i):
                with open(i, "r") as f:
                    if (
                        open(
                            f"{UserHome}/Eat-PKG-Manager/{posix_tools.path.basename(i)}",
                            "r",
                        ).read()
                        != open(
                            f"{UserHome}/comparison_eat_both/{posix_tools.path.basename(i)}",
                            "r",
                        ).read()
                    ):
                        c.stdout.flush
                        c.stdout.write(
                            f"\r{Fore.YELLOW}Warning:{Style.RESET_ALL} Not up to date. Upgrade to the latest version now.\n"
                        )
                        print("Outdated files in root of eat:")
                        for i in glob.glob(f"{UserHome}/Eat-PKG-Manager/*"):
                            if (
                                posix_tools.path.isfile(i)
                                and open(
                                    f"{UserHome}/Eat-PKG-Manager/{posix_tools.path.basename(i)}",
                                    "r",
                                ).read()
                                != open(
                                    f"{UserHome}/comparison_eat_both/{posix_tools.path.basename(i)}",
                                    "r",
                                ).read()
                            ):
                                print(f" • {posix_tools.path.basename(i)}")
                        c.stdout.flush()
                        break
                    else:
                        c.stdout.flush()
    except Exception as e:
        print(f"{Fore.YELLOW}Warning:{Style.RESET_ALL} Update check error: {e}")
    shutil.rmtree(f"{UserHome}/comparison_eat_both")
print(f"Installing {args.target}...")
if posix_tools.geteuid() != 0:
    if gi:
        print(
            f"{Fore.RED}Error:{Style.RESET_ALL} You must be root to install apps globally."
        )
        exit(1)
elif args.system:
    globalInstall = 1
if not posix_tools.path.isfile(f"{UserHome}/eat_sources/{args.target}.yaml"):
    print(
        f"{Fore.RED}Error [EAT_ERROR_NO_MANIFEST error code 0x80]:{Style.RESET_ALL} Could not find the program \"{args.target}\". This is not my fault, it's the network's\nfault. The network is open-source, feel free to add your own manifests:\n     > https://github.com/Tyler887/eat-network/fork\nor see a list of avaliable packages:\n     > https://github.com/Tyler887/eat-network/tree/main\nHappy packaging! :)\n{Fore.LIGHTBLACK_EX}Note: You might have outdated sources, try upgrading them by running:\nbash ~/Eat-PKG-Manager/update.sh"
    )
    exit(1)
with open(f"{UserHome}/eat_sources/{args.target}.yaml", "r") as manifest:
    global packageUri
    global packageRequiresAdmin
    global packageSuggestions
    global packageRequirements
    global packageBinary
    convertedManifest = yaml.full_load(
        manifest.read()
    )  # Convert YAML manifest to Python dictionary
    try:
        packageUri = convertedManifest["uri"]
    except KeyError:
        print(
            f"{Fore.RED}Error:{Style.RESET_ALL} You must set a URI for the package. Set 'uri' in the manifest."
        )
        exit(1)
    if not packageUri.endswith(".zip") and not packageUri.endswith(".tar.gz"):
        print(
            f"{Fore.RED}Error:{Style.RESET_ALL} Only zip and gzip-tarred packages are compatible with eat at the moment."
        )
        exit(1)
    try:
        packageRequiresAdmin = convertedManifest["sudo_necessary"]
    except KeyError:
        packageRequiresAdmin = False
    if packageRequiresAdmin and posix_tools.geteuid() != 0:
        print(
            f"{Fore.RED}Error [EAT_PROGRAM_TOUCHES_SYSTEM error code 3x76]:{Style.RESET_ALL} Installing this package requires root access, maybe try running:\n      sudo python3 {UserHome}/Eat-PKG-Manager/eat-install.py {args.target} --system"
        )
        exit(1)
    try:
        packageRequirements = convertedManifest["depends"]
    except KeyError:
        packageRequirements = []
    for i in packageRequirements:
        if not posix_tools.path.isdir(f"{UserHome}/eat_app_{i}"):
            print(
                f"{Fore.RED}Error [EAT_PROGRAM_REQURIRES_{i.upper()} error code 8x42]:{Style.RESET_ALL} This package requires other packages in order to function.\nPlease install them and try again.\nThe first package detected was: {i}"
            )
            print("\nYou need the following packages to install {args.target}:")
            for i in packageRequirements:
                print(f" • {i}")
            exit(1)
    try:
        packageSuggestions = convertedManifest["should_install"]
    except KeyError:
        packageSuggestions = []
    for i in packageSuggestions:
        if not posix_tools.path.isdir(f"{UserHome}/eat_app_{i}"):
            print(
                f"{Fore.YELLOW}Warning:{Style.RESET_ALL} The following unavaliable package is recommended for {args.target}: {i}"
            )
    url = packageUri
    print("Moving to user directory.")
    if url.endswith(".zip"):
        download(url, f"{UserHome}/eat_pack_{args.target}.zip")
    else:
        download(url, f"{UserHome}/eat_pack_{args.target}.tar.gz")
    with open(f"{UserHome}/eat_pack_{args.target}.zip", "wb") as file:
        print("Extracting to app directory.")
        if url.endswith(".zip"):  # Zipped
            with zipfile.ZipFile(
                f"{UserHome}/eat_pack_{args.target}.zip", "r"
            ) as zip_ref:
                zip_ref.extractall(f"{UserHome}/eat_app_{args.target}")
            posix_tools.unlink(f"{UserHome}/eat_pack_{args.target}.zip")
        else:  # Tarred, uses same engine as zip, see https://stackoverflow.com/questions/39265680/how-to-convert-tar-gz-file-to-zip-using-python-only
            tarf = tarfile.open(
                name=f"{UserHome}/eat_pack_{args.target}.tar.gz", mode="r|gz"
            )
            zipf = zipfile.ZipFile(
                file=f"{UserHome}/eat_pack_{args.target}.zip",
                mode="a",
                compression=zipfile.ZIP_DEFLATED,
            )
            for m in tarf:
                tarx = open(tarf.extractfile(m), "w+")
                fl = tarx.read()
                fn = m.name
            zipf.writestr(fn, fl)
            tarf.close()
            zipf.close()
            with zipfile.ZipFile(
                f"{UserHome}/eat_pack_{args.target}.zip", "r"
            ) as zip_ref:
                zip_ref.extractall(f"{UserHome}/eat_app_{args.target}")
            posix_tools.unlink(f"{UserHome}/eat_pack_{args.target}.zip")
            posix_tools.unlink(f"{UserHome}/eat_pack_{args.target}.tar.gz")
        packageBinary = "n/a"
        for i in glob.glob(f"{UserHome}/eat_app_{args.target}/*"):
            if is_binary_string(
                open(i, "rb").read(1024)
            ):  # https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
                if not "." in os.path.basename(
                    i
                ):  # https://stackoverflow.com/a/40439696
                    packageBinary = i
                    break
        if packageBinary == "n/a":
            print(
                f"{Fore.YELLOW}Warning:{Style.RESET_ALL} No binaries found! You may need to compile this program manually and update .bashrc as required to use this app."
            )
        with open(f"{UserHome}/.bashrc", "w") as bashrc:
            if not packageBinary == "n/a":
                if gi:
                    os.system(f"install {packageBinary}")
                else:
                    bashrc.write(
                        f"\n# add command for {args.target}\nalias {args.target}='{UserHome}/eat_app_{args.target}/{packageBinary}'"
                    )
        print(f"{Fore.GREEN}Installed {args.target}{Style.RESET_ALL}!")
