##Download movielens data and process it
from urllib.request import urlopen
from zipfile import ZipFile
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



def main():
    DATASET_URL="https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    # Download the file from the URL
    zipresp = urlopen(DATASET_URL)
    # Create a new file on the hard drive
    tempzip = open("tempfile.zip", "wb")
    # Write the contents of the downloaded file into the new file
    tempzip.write(zipresp.read())
    # Close the newly-created file
    tempzip.close()
    # Re-open the newly-created file with ZipFile()
    zf = ZipFile("tempfile.zip")
    # Extract its contents into <extraction_path>
    # note that extractall will automatically create the path
    zf.extractall(path = '.')
    # close the ZipFile instance
    zf.close()
    os.remove("tempfile.zip")

if __name__=="__main__":
    main()