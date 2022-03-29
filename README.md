# `eat`
The package manager for Linux.
## Install
Simple (this script was made for BASH):
```bash
git clone htttps://github.com/Tyler887/eat
cd eat
bash ./inst-script.sh
# Then, restart your shell and run 'eathelp' for the manpage
```
If `git` does not seem to be a command (which you can look for by running `which git`), you can run:
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/Tyler887/eat/main/inst-script.sh -#)"
```
You have not installed `eat` if you get something like this:
```
Command 'eat' not found, did you mean:

  command 'pat' from deb dist (1:3.5-236-0.1build1)
  command 'dat' from deb liballegro4-dev (2:4.4.3.1-1)
  command 'eet' from deb libeet-bin (1.23.3-8)
  command 'at' from deb at (3.1.23-1ubuntu1)
  command 'bat' from deb bacula-console-qt (9.4.2-2ubuntu5)
  command 'heat' from deb python3-heatclient (2.1.0-0ubuntu1)
  command 'neat' from deb neat (2.2-1build1)
  command 'ear' from deb ecere-dev (0.44.15-1build3)
  command 'iat' from deb iat (0.1.3-7build1)
  command 'cat' from deb coreutils (8.30-3ubuntu2)
  command 'ent' from deb ent (1.2debian-2)

Try: sudo apt install <deb name>
```
Usally, `eat` only works in BASH shells. If you would like to edit your shell's own init script, run:
```bash
nano .<shell>rc
```
### Ubuntu recovery mode install
1. Hold <kbd>Shift</kbd> on boot until the GRUB2 menu appears.
2. Select `Advanced options for Ubuntu` and choose the second option.
3. When Ubuntu starts up recovery mode, select `network` then confirm with "Yes".
   This is because Git and APT cannot reach the internet without networking mode.
5. Select `root` after networking mode for Recovery Mode is set up, then enter `root`'s password.
6. Run `su <your own UNIX user name>` to actually install to your user (else `eat` only works for the `root` user).
7. Follow the steps above.
8. Run `reboot`, hold <kbd>Shift</kbd>, select `Advanced options for Ubuntu` -> the second option, select `network` > `Yes` > `root`, enter `root`'s password, run `su <your own UNIX user name>`, and try it out using `eatinst setup-eat`. This will usally initiate the sources, because there's no `setup-eat.yaml` in the manifest network.
9. `reboot` your system without going into GRUB.
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

A manifest must be named `<manifest name>.yaml`, not something like `<manifest name>.json` or `<manifest name>.yml`.
