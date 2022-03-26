import os, glob

for i in glob.glob(f"{os.getcwd()}/*.py"):
    os.system(f"black {i}")
