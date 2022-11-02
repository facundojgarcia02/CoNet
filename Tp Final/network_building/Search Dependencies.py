import json
import requests
import warnings

from glob import glob
from tqdm import tqdm


# PARAMS:
jsons_path = input("Path for saving jsons: ")

# Move to package names folder and find all files.
files = sorted(glob(jsons_path + "\*"))

def get_package_name(path):
    package_name = path.split("\\")[-1]
    package_name = package_name[:-5]
    return package_name

def parse_deps(deps):
    if deps is None:
        return []
    
    proc_deps = []
    for dep in deps:
        dep = dep.replace(">", " ")
        dep = dep.replace("<", " ")
        dep = dep.replace("=", " ")
        dep = dep.replace(";", " ")
        dep = dep.split(" ")[0]
        proc_deps.append(dep)
    
    return proc_deps

network_data = []
packages_with_error = []
i = 0
for filename in tqdm(files):
    with open(filename, "r") as f:
        package_name = get_package_name(filename)

        try:
            package_info = json.load(f)
            package_deps = parse_deps(package_info["info"]["requires_dist"])
            package_tags = package_info["info"]["keywords"]
            package_license = package_info["info"]["license"]
            package_version = package_info["info"]["version"]
            package_python_v = package_info["info"]["requires_python"]
            package_classifiers = package_info["info"]["classifiers"]
            package_last_version_date = package_info["releases"][package_version]["0"]["upload_time"]
            package_dict = {"Name": package_name, 
                            "Dependencies": package_deps, 
                            "Tags": package_tags, 
                            "Licence": package_license, 
                            "Package Version": package_version,
                            "Python Version": package_python_v,
                            "Classifiers": package_classifiers}
            network_data.append(package_dict)

        except KeyError as e:
            packages_with_error.append(package_name)


with open("proc_jsons.json", "w") as f:
    json.dump(network_data, f)
print("Saved processed JSON´s.")

"""
# Search not found packages.
not_found_packages = []
package_names = [p["Name"] for p in network_data]
for p in tqdm(network_data):
    for dep in p["Dependencies"]:
        if (dep.lower() not in package_names) and (dep.lower() not in not_found_packages):
            not_found_packages.append(dep.lower())
"""

# Save not found JSONS
with open("Packages with error.txt", 'w') as fp:
    for item in packages_with_error:
        fp.write("%s\n" % item) #Write each element in a new line.

print('Saved not found libraries.')