import subprocess
import sys
from tqdm import tqdm
import os

class DownloadHandler():

    def __init__(self, verbose = True, downloaded_whls_filename: str = None,
                 whls_path = None):
        self.verbose = verbose

        if downloaded_whls_filename is not None:
            import pickle
            with open(downloaded_whls_filename, "rb") as f:
                results = pickle.load(f)
                self.downloaded = results["downloaded"]
                self.not_downloaded = results["not-downloaded"]

        else:
            print("Starting from 0")
            self.not_downloaded = []
            self.downloaded = []
        
        if whls_path is None:
            raise ValueError("Required 'whls_path'.")
        os.chdir(whls_path)

    def download(self, package):
        if (not package in self.downloaded) and (not package in self.not_downloaded):
            if self.verbose: print(f"Downloading {package}.")
            try:
                subprocess.check_call(["pip", "download", package, "--quiet", "--no-cache-dir"])
                self.downloaded.append(package)

            except subprocess.CalledProcessError:
                self.not_downloaded.append(package)

            if self.verbose: print(f"{package} downloaded.")

    def multi_download(self, packages):

        for pkg in tqdm(packages):
            self.download(pkg["name"])

    def drop_results(self):
        results = {"downloaded": self.downloaded, "not-downloaded": self.not_downloaded}

        import pickle
        with open("downloaded-wheels.status", "wb") as f:
            pickle.dump(results, f)

if __name__ == "__main__":
    import json
    
    master_path = r"C:\Users\juanm\OneDrive\Documentos\GitHub\CoNet\Tp Final\network_building\status_files" #Current .py dir
    whls_path = r"D:\whls" #dir for saving whls files.

    os.chdir(whls_path)

    #Open packages data, init downloader and download all packages.
    with open(master_path + r"\pypi-packages.json", "r") as f:
        packages = json.load(f)

    downloader = DownloadHandler(
        verbose=False, 
        downloaded_whls_filename = master_path+r"\downloaded-wheels.status",
        whls_path = whls_path)
    
    downloader.multi_download(packages)
    
    #Save results
    os.chdir(master_path)
    downloader.drop_results()