import os, glob
for i in glob.glob(f"{os.getcwd()}/*.py"):
  print(f"Linting {i}...")
  os.system(f"black {i}")
