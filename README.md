[store]: https://github.com/EatInstall/Store
# <code><sup>e</sup>a<sub>t</sub></code>

[![Status](https://img.shields.io/badge/status-alpha-red)](https://github.com/Tyler887/eat/commits/main) [![GitHub download](https://img.shields.io/github/downloads/Tyler887/eat/total)](https://github.com/Tyler887/eat/releases) [![License](https://img.shields.io/github/license/Tyler887/eat)](https://github.com/Tyler887/eat/blob/main/LICENSE) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Eat is the package manager for Linux. It:
* **Does not even require  `sudo`!**
* Adds the programs to your PATH
* Does total web scraping to download files
* Makes sharing Linux programs easier

Here's how I would use Eat: `eatinst pwsh`

While Eat is specific to Debian and Ubuntu, Eat can be installed and ran on
almost any Linux distribution. Eat provides rootless install, so you don't
have to use the `root` user when you need to install software. And if you use
`sudo`, you can globally install programs to `/usr/bin` with the long complex command
`sudo python3 /home/$(whoami)/eat-install.py --system <program>` (pretty advanced).
## Install
Simple:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/EatInstall/EatInstaller/HEAD/eatinstaller.sh)"
```
Usally, `eat` only works in BASH shells. If you would like to edit your shell's own init script, run:
```bash
nano .<shell>rc
```
If you are a developer and want to install Eat (through the dev branch) in your GitHub Actions CI, add
this as the first step:
```yaml
- name: Install Eat
  uses: EatInstall/GitHub-Setup@v1.1
```
### ⚙️ Eat as a Service (EaaS) [[more info](https://github.com/EatInstall/Eat/pkgs/container/eat)]
Running Eat on a container is *simple*:
```bash
docker pull ghcr.io/eatinstall/eat:dev
```
**Note: This method installls from the `dev` branch. It is highly recommended to do a proper install instead.**
### Legacy installer
The legacy installer can still be run on Debian, if you cannot run the new GUI version:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/EatInstall/Eat/HEAD/inst-script.sh)"
```
This script only works on Debian and it's derivatives. If you do not use any of the derivatives or
Debian itself, you must use [EatInstaller](#install).
## Upgrading
If your installation is out of date (which Eat normally tells you) or you have out-of-date sources,
you should upgrade both of them.

To upgrade Eat and the source manifests, the fastest way is to run `bash ~/Eat-PKG-Manager/update.sh`.
Using `git pull` also works, but your sources will need to be upgraded manually.
## New manifests
A manifest goes into the [network](https://github.com/Tyler887/eat-network), and not in this repo.
To add more manifests to eat, please contribute there.

The specification of an Eat package is:
```yaml
uri: # URI for package archive (.zip or .tar.gz). Eat will not install packages without this.
depends:
   - # Array of dependencies. Eat will fail installation if one of these are not installed. Empty by default
should_install:
   - # Array of suggested packages (e.g. "soft dependencies"). Empty by default
sudo_necessary: # Whether the app touches the system or not. "true" or "false" accepted only. Default is "false"
```

Yes, it's a YAML manifest.
A manifest must be named `<manifest name>.yaml`, not something like `<manifest name>.json` or `<manifest name>.yml`.
## Store
If you do not use a command-line for installing programs (other than eat itself), we offer [Eat Store][store]
for installing apps.
## Authors
Eat was originally written by [Tyler887](https://github.com/Tyler887), but a [mass migration to this organisation](https://github.com/EatInstall/Eat/pull/4)
was preformed.
## License
Eat is licensed under the [GNU General Public License](https://gnu.org/licenses/gpl-3.0.html).
You can read the full text by viewing the [LICENSE](./LICENSE) file.

This means we reserve the right to relicense Eat under another license, e.g. an EULA.
But it's fine to port Eat to proprietary OSes, but the conditions of the GPL still apply.
