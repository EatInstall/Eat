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
