# wf-attack-vpn
This is the code used for the master thesis "The Effect Background Traffic in VPNs has on Website Fingerprinting", published 2023 june the 15th by Gustav Rehnholm. It is used to create simulate VPN traffic with foreground and background traffic, to test how Website fingerprinting (WF) is effected by background traffic. It is made to make use of already existing datasets. The foreground dataset used, and the implemented WF attack, is both provided by Tobias Pulls, and the background dataset consist of one from MIT, and one from KAU.

## Table of contents
1. [Setup](#setup)
    1. [Python Packages](#lib)
    2. [MIT Dataset](#mit)
    3. [KAU Dataset](#kau)
    4. [Directories](#dir)
2. [Project Structure](#struct)
    1. [data_analysis](#data_analysis)
    2. [get_old_result_twitch](#get_old_result_twitch)
    3. [merge_traffic](#merge_traffic)
    4. [parse_background](#parse_background)
    5. [plot_graphs](#plot_graphs)
    6. [train_test_combinations](#train_test_combinations)
    7. [Undefended](#Undefended)
    8. [wf-attack](#wf-attack)
3. [Contact Information](#Contact)
4. [Bibtex Citation](#bibtex)
5. [License](#License)



## Setup <a name="setup"></a>
To setup the enviroment to recreate the result, one needs to add some directories in the cwd, download the dataset from MIT, the Twitch traffic and foreground traffic from KAU. Also download the necessary python packages. To run the Website Fingerprinting, one needs besides python packages, also an implementation of deep fingerprinting and Tik-Tok, which has been provided by Tobias Pulls. 

### Python Packages <a name="lib"></a>
Bellow is shown the packages needed to run the scripts, how to install them, and links with a more indept description on how to install them. 

[Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html):
```bash 
pip install pandas 
```

[pytables](https://www.pytables.org/usersguide/installation.html):
```bash 
pip install numpy
pip install numexpr
pip install Cython
pip install blosc
pip install blosc2
pip install tables 
```

[Seaborn](https://seaborn.pydata.org/installing.html):
```bash 
pip install matplotlib 
pip install seaborn
```

[PyTorch](https://pytorch.org/get-started/locally/):
```bash 
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
Miniconda3-latest-Linux-x86_64.sh 
```

After installing all packages, log out and log in again, and then run (can take some time):

```bash
 conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia 
 ```

### MIT Dataset <a name="mit"></a>
The MIT dataset can be found [here](https://www.ll.mit.edu/r-d/datasets/vpnnonvpn-network-application-traffic-dataset-vnat), and is stored as h5 file, and pcap files. Both contain the same information, so one do only need the h5 file. It can be downloaded with wget, and make sure that the file is named VNAT_Dataframe_release_1.h5, as it is the name that the scripts is expecting.

```bash
wget https://archive.ll.mit.edu/datasets/vnat/VNAT_Dataframe_release_1.h5
```

### KAU Dataset <a name="kau"></a>
At KAU, Tobias Pulls has generated the foreground traffic, and the twitch traffic has been generated by Christoffer Sandquist and Jon-Erik Ersson, for their bachelor at KAU (2023). Both can be downloaded by running the following: 
```bash
wget http://dart.cse.kau.se/dataset-wg-ff-week15-92-sites-avg-100-samples-merged-cut.zip
wget dart.cse.kau.se/rds-collect/twitch.zip
```

### Directories <a name="dir"></a>
* ``` stdout ```
    * for all text output from the programs
* ``` h5 ```
    * the extracted MIT datasets
* ``` twitch/parsed_captures ```
    * for the parsed twitch captures, in log files
* ``` twitch/merged_captures ```
    * for the merged twitch captures, as h5 files 


## Project Structure <a name="struct"></a>
This project is divided in different directories for the different steps needed for the analysing WF. This section will in short describe the role of each directory.

### data_analysis <a name="data_analysis"></a>
This is to analyse the background datasets, the foreground, the simulated dataset, and to get statistics from the WF results. 
License
### get_old_result_twitch <a name="get_old_result_twitch"></a>
To recreate the result from Errsons and Sandquist work.

### merge_traffic <a name="merge_traffic"></a>
To merge background and froeground into a simulated dataset

### parse_background <a name="parse_background"></a>
To parse the gathered background dataset, each source (KAU, MIT), has its own directory

### plot_graphs <a name="plot_graphs"></a>
To creeate graphs from the WF results

### train_test_combinations <a name="train_test_combinations"></a>
To get the simulated datasets, where the advesary does not have access to the same background traffic as is in the testing dataset.

### Undefended <a name="Undefended"></a>
To get result of an 10-fold on only the foreground without any background. 

### wf-attack <a name="wf-attack"></a>
Scripts to run all WF attacks.

## Contact Information <a name="Contact"></a>
If one have any questions, contact Gustav Rehnholm at: gustav.rehnholm.docetic@8shield.net

## Bibtex Citation <a name="Bibtex"></a>
@mastersthesis{rehnholm,
  author  = {Rehnholm, Gustav},
  title   = {The Effect Background Traffic in VPNs has on Website Fingerprinting},
  school  = {Karlstads University},
  year    = {2023},
  month   = jun
}

## License <a name="License"></a>
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)

