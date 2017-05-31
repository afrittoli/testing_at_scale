#!/bin/bash -e
# Download files from logs.openstack.org

BASE_URL=http://logs.openstack.org
# This folder should contain a list of runs
BASE_PATH=${1:-periodic/periodic-tempest-dsvm-neutron-full-test-accounts-ubuntu-xenial-master}
FILE_REGEX=${2:-screen-n-cpu.txt.*}
RELATIVE_PATH=${3:-logs}

# Get the list of runs first
echo "Generating run folders"
wget --quiet -nH --cut-dirs=1 -e robots=off -r --no-parent --accept-regex '([0-9a-b]*|logs|gz)$' --reject 'index.html*' $BASE_URL/$BASE_PATH/ -l 1
DOWNLOAD_FOLDER=$(basename $BASE_PATH)

# Generate a list of files to be downloaded
echo "Generating the list file"
rm ${DOWNLOAD_FOLDER}_list.txt || true
for run in $(ls $DOWNLOAD_FOLDER); do
  echo "$BASE_URL/$BASE_PATH/$run/$RELATIVE_PATH/" >> ${DOWNLOAD_FOLDER}_list.txt
done

# Download the files that match regex
echo "Downloading logs"
wget --quiet -nH --cut-dirs=1 -e robots=off -r --no-parent --accept-regex '([0-9a-b]*|logs|gz)$' --reject 'index.html*' --accept "$FILE_REGEX" -l 1 -i ${DOWNLOAD_FOLDER}_list.txt
