from inspect import Attribute
import pkginfo
import pickle

from os import listdir, chdir
from os.path import isfile, join
from tqdm import tqdm

master_path = r"C:\Users\juanm\OneDrive\Documentos\GitHub\CoNet\Tp Final\network_building\status_files"
whls_path = r"D:/whls"

#Get whls files.
chdir(whls_path)
files = [f for f in listdir(r"D:/whls") if isfile(join(whls_path, f))]

#Search dependencies with pkginfo for every file in folder.
dependencies = {}
for wheel_fname in tqdm(files):
    try:
        metadata = pkginfo.get_metadata(wheel_fname)
        deps = metadata.requires_dist
        dependencies[metadata.name] = [dep.split(" ")[0] for dep in deps]
    except AttributeError: #Error for some wheels.
        print(wheel_fname, "is not defined correctly.")

#Save results.
chdir(master_path)
with open("found_dependencies.status","wb") as f:
    pickle.dump(dependencies, f)