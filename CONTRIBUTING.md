# Contributing to `eat`
Looking to contribute to `eat`? **Okay!** As a practice, you should read these guiddelines before contributing.
## Guidelines
`eat` automatically formats itself to comply with PEP-8. Please always format your code:
```bash
python -m pip install black
python -m black
```
If you do not do this, it will be done instantly on merge by the CI.

Do not take code of the Linux kernel to prevent  `GPL-2.0-only` violations. Eat is written in Python, while Linux the
kernel is written in C.

Don't make `install` part of CoreUtils get executed. This is for security reasons. Executing other programs from `coreutils` is fine.

Additionally:
* The Eat CLI does not handle any manifests in this repo. Please submit your manifests to
  <code>EatInstall/[Network](https://github.com/EatInstall/Network)</code>.
* Do not modify `private` in `settings.yml` in the `.github` folder. This repo should be
  public forever.
* Follow the [Python 3.10](https://docs.python.org/3.10) standards. That means **no Python
  2.7 code!**
