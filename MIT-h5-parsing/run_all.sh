# basic script to run from start to end


# Extract VPN traffic, and store them depending on the application
python wf-attack-vpn/MIT-h5-parsing/extract_dataset.py

# analysis of the extracted data
python wf-attack-vpn/MIT-h5-parsing/extract_dataset_analysis.py