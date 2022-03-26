# license: GPL-3.0-or-later (with some CC-licensed code snippets, follow links for more info)
import os as posix_tools
import argparse
import sys as c
import colorama
import urllib.request
import zipfile, tarfile
import yaml # PyYAML
import shutil

parser = argparse.ArgumentParser(prog="Eat Utilities", usage="eatinst target [options]")

parser.add_argument('target', type=str,
                    help='package to install')
parser.add_argument('-d', action="store_true",
                    help='download only, don\'t install')
args = parser.parse_args()

c.stdout.write("\rCollecting sources...")
# Credit: https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
# License: https://stackoverflow.com/help/licensing
url = 'https://github.com/Tyler887/eat-network/releases/latest/download/sources.zip'
response = urllib.request.urlopen(url)
data = response.read()      # a `bytes` object
text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
c.stdout.flush()
c.stdout.write("\rMoving sources archive to user directory...")
with open("~/eat_sources.zip", "w") as file:
  f.write(text)

c.stdout.flush()
c.stdout.write("\rUnzipping downloaded source archives...                 ") # the whitespace is  necessary to prevent unexpected text spill lol

# Credit: https://stackoverflow.com/a/49063295
# see license at the top of the code of Eat
with zipfile.ZipFile("~/eat_sources.zip", 'r') as zip_ref:
    zip_ref.extractall("~/eat_sources")
posix_tools.unlink("~/eat_sources.zip")

print(f"\nEat Utilities: {Fore.GREEN}Completed retrevial of sources!{Style.RESET_ALL}")

print(f"Installing {args.target}...")
if not posix_tools.path.isfile(f"~/eat_sources/{args.target}.yaml"):
   print(f"{Fore.RED}Error:{Style.RESET_ALL} No such manifest in Eat network. The network is open-source, feel free to add your own manifests:\nhttps://github.com/Tyler887/eat-network")
   exit(1)
with open(f"~/eat_sources/{args.target}.yaml", "r") as manifest:
  global packageUri
  global packageRequiresAdmin
  global packageSuggestions
  global packageRequirements
  convertedManifest = yaml.full_load(manifest.read()) # Convert YAML manifest to Python dictionary
  packageUri = convertedManifest['uri']
  if not packageUri.endswith(".zip") and not packageUri.endswith(".tar.gz"):
      print(f"{Fore.RED}Error:{Style.RESET_ALL} Only zip and gzip-tarred packages are compatible with eat at the moment.")
      shutil.rmtree("~/eat_sources")
      exit(1)
  packageRequiresAdmin = convertedManifest['sudo_necessary']
  if packageRequiresAdmin and posix_tools.geteuid() != 0:
     shutil.rmtree("~/eat_sources")
     print(f"{Fore.RED}Error:{Style.RESET_ALL} Installing this package requires root access, maybe try with sudo?")
     exit(1)
  packageRequirements = convertedManifest['depends']
  for i in packageRequirements:
     if not posix_tools.path.isdir(f"~/eat_app_{i}"):
        shutil.rmtree("~/eat_sources")
        print(f"{Fore.RED}Error:{Style.RESET_ALL} This package requires other packages in order to function. Please install them and try again.\nThe first package detected was: {i}")
        exit(1)
  packageSuggestions = convertedManifest['should_install']
  for i in packageSuggestions:
        if not posix_tools.path.isdir(f"~/eat_app_{i}"):
            print(f"{Fore.YELLOW}Warning:{Style.RESET_ALL} The following package is recommended for {args.target}: {i}")
  url = packageUri
  response = urllib.request.urlopen(url)
  data = response.read()      # a `bytes` object
  text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
  print("Moving to user directory.")
  with open(f"~/eat_pack_{args.target}.zip", "w") as file:
    f.write(text)
  if args.d:
    print(f"Downloaded {args.target}!")
  else:
    print("Extracting to app directory.")
    if url.endswith(".zip"): # Zipped
      with zipfile.ZipFile(f"~/eat_pack_{args.target}.zip", 'r') as zip_ref:
        zip_ref.extractall(f"~/eat_app_{args.target}")
      posix_tools.unlink(f"~/eat_pack_{args.target}.zip")
    else: # Tarred, uses same engine as zip, see https://stackoverflow.com/questions/39265680/how-to-convert-tar-gz-file-to-zip-using-python-only
      tarf = tarfile.open( name=f'eat_pack_{args.target}.tar.gz', mode='r|gz' )
      zipf = zipfile.ZipFile( file=f'~/eat_pack_{args.target}.zip', mode='a', compression=zipfile.ZIP_DEFLATED )
      for m in tarf:
        f = tarf.extractfile( m )
        fl = f.read()
        fn = m.name
      zipf.writestr( fn, fl )
      tarf.close()
      zipf.close()
      with zipfile.ZipFile(f"~/eat_pack_{args.target}.zip", 'r') as zip_ref:
        zip_ref.extractall(f"~/eat_app_{args.target}")
      posix_tools.unlink(f"~/eat_pack_{args.target}.zip")
      posix_tools.unlink(f"~/eat_pack_{args.target}.tar.gz")
    posix_tools.system(f"export PATH=~/eat_app_{args.target}:$PATH")
    print(f"Installed {args.target}!")
shutil.rmtree("~/eat_sources")
