'''
Get duration of the different applications and categories for the MIT dataset
To determine if the lacking of data in the h5 file, is also present in the pcap files

touch stdout/get_duration.txt
python wf-attack-vpn/MIT-pcap-parsing/get_duration.py | tee stdout/get_duration.txt
'''
# to read the pcap files
from pcapfile import savefile
import dpkt
# to get the pcap files in their directory 
import os

YOUTUBE_INDEX = 0
SFTP_INDEX    = 1
SKYPE_INDEX   = 2
SSH_INDEX     = 3
RDP_INDEX     = 4
RSYNC_INDEX   = 5
VOIP_INDEX    = 6
SCP_INDEX     = 7
NETFLIX_INDEX = 8
VIMEO_INDEX   = 9

APPLICATIONS = ['youtube', 'sftp', 'skype-chat', 'ssh', 'rdp', 'rsync', 'voip', 'scp', 'netflix', 'vimeo']


def main():
    print("Start analyze of pcap files from MIT")

    DIRECOTRY = "VNAT_release_1"

    # information about the dataset as a whole
    # number of captures in total, that are vpn and that are not vpn traffic
    nr_of_captures   = 0
    nr_of_vpn        = 0
    nr_of_nonvpn     = 0

    duration_dic = {
        'youtube' : [],
        'sftp' : [],
        'skype-chat': [],
        'ssh': [],
        'rdp': [],
        'rsync': [],
        'voip': [],
        'scp': [],
        'netflix': [],
        'vimeo': []
    }

    duration_list = []

    for file in os.listdir(DIRECOTRY):
        nr_of_captures += 1
        filename = os.fsdecode(file)

        if not filename.endswith(".pcap"): 
            print("ERROR: the file (" + str(filename) + ") should not be part of the directory")
            return

        if filename.startswith("nonvpn"):
            nr_of_nonvpn += 1
            continue
        elif filename.startswith("vpn"):
            nr_of_vpn += 1
            for i in range(0, len(APPLICATIONS)):
                if APPLICATIONS[i] in filename:
                    duration_dic[APPLICATIONS[i]].append(getTimeStamps(DIRECOTRY, filename))
        else:
            print("ERROR: filename did not start with vpn or nonvpn, ABORT program")
            print(filename)
            return

    print_durations(duration_dic)

       
    return

# Get duration for the provided pcap file
def getTimeStamps(dir, pcap_file):
    list_dur = []
    file_dir = dir + "/" + pcap_file
    opened_file = open(file_dir, 'rb')

    for ts, pkt in dpkt.pcap.Reader(opened_file):
        list_dur.append(ts)
    '''
    capfile = savefile.load_savefile(testcap, verbose=True)

    for pkt in capfile:
        list_dur.append(pkt.timestamp)
    '''
    
    return list_dur


# print the different durations that are relevant in hours (input should be in seconds)
def print_durations(duration_dic):
    # list of all applications durations, in hours
    duration_list = []
    for j in duration_dic:
        #sort(duration_dic[APPLICATION[j]])
        duration_sec = duration_dic[APPLICATION[j]][-1] - duration_dic[APPLICATION[j]][0]
        duration_list[j] = duration_sec / (60 * 60)
    
    # The relevant durations
    total_duration         = sum(duration_list)
    streaming_duration     = duration_list[VIMEO_INDEX] + duration_list[NETFLIX_INDEX] + duration_list[YOUTUBE_INDEX]
    voip_duration          = duration_list[VOIP_INDEX]
    chat_duration          = duration_list[SKYPE_INDEX]
    c2_duration            = duration_list[SSH_INDEX] + duration_list[RDP_INDEX]
    file_transfer_duration = duration_list[SFTP_INDEX] + duration_list[RSYNC_INDEX] + duration_list[SCP_INDEX]
    

    print("")
    print("--------------------------------------------------------------")
    print("Duration for each application")
    print("")
    for i in duration_list:
        print(str(APPLICATION[i]) + ":" + str(duration_list[i]))
    print("--------------------------------------------------------------")
    print("Duration for each category")
    print("")
    print("Streaming VPN noise(h): " + str(streaming_duration))
    print("Chat VPN noise(h): " + str(chat_duration))
    print("c2 VPN noise(h): " + str(c2_duration))
    print("file transfer VPN noise(h): " + str(file_transfer_duration))
    print("voip VPN noise(h): " + str(voip_duration))
    print("")
    print("Total VPN noise(h): " + str(total_duration))
    print("--------------------------------------------------------------")
    print("Duration, in percent, for each category")
    print("")
    print("Streaming: " + str((streaming_duration / total_duration) * 100))
    print("Chat: " + str((chat_duration / total_duration ) * 100))
    print("c2: " + str((c2_duration / total_duration) * 100))
    print("file transfer: " + str((file_transfer_duration / total_duration) * 100))
    print("voip: " + str((voip_duration / total_duration) * 100)) 


if __name__=="__main__":
    main()