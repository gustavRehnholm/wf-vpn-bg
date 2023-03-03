# wf-attack-vpn
To test website fingerprinting attacks when merging regular VPN web traffic with VPN noise, generated by MIT, and KAU.


## Setup
Need to download the dataset form MIT, the noise form KAU, and the regular web traffic. Also download the necessary python packages. To run the Website Fingerprinting, one needs besides python packages, also the implementation of deep fingerpritnig, whcih is proivded by Tobias Pulls. 

In the cwd, one needs top add some direcotries, to store the results from the program.

### Python Packages
need pandas:
* pip install pandas

but also pytable and its dependencies as described in (https://www.pytables.org/usersguide/installation.html):
* numpy
    * pip install numpy
* numexpr
    * pip install numexpr
* cython
    * pip install Cython
* c-bloscchoco
    * pip install blosc
* python-blosc2
    * pip install blosc2
* pytables
    * pip install tables

To run the website fingerpritning, one need to install pytorch through anaconda:
* wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
* bash Miniconda3-latest-Linux-x86_64.sh
* log out and log in again, then run (can take ages)
* conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia

### MIT data
The data can be found at (https://www.ll.mit.edu/r-d/datasets/vpnnonvpn-network-application-traffic-dataset-vnat), and is stored as h5 file, and pcap files. Both contain the same information, so one do only need the h5 file.
* download the h5 file
    * wget https://archive.ll.mit.edu/datasets/vnat/VNAT_Dataframe_release_1.h5
    * name the file: VNAT_Dataframe_release_1.h5
* download the pcap files
    * wget https://www.ll.mit.edu/r-d/datasets/vpnnonvpn-network-application-traffic-dataset-vnat
    * name the dir: VNAT_release_1

### Kau data
At KAU, Tobias Pulls has generated the regular web traffic, and the twitch traffic has been generated by Christoffer Sandquist and Jon-Erik Ersson, for their bachelor at KAU (2023).
* download the web traffic
    * wget http://dart.cse.kau.se/dataset-wg-ff-week15-92-sites-avg-100-samples-merged-cut.zip
    * name the dir: dataset
* download the twitch traffic
    * wget dart.cse.kau.se/rds-collect/twitch.zip
    * name the dir: captures

### directories
* stdout
    * for all text output from the programs
* h5
    * the extracted MIT datasets
* twitch/merged_captures
* twitch/parsed_captures

