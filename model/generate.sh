#========================================================
#
#        Introduction to artificial intelligence
#
#                         PacNET
#
#========================================================
# @ Victor Mangeleer - S181670
#
#--------------
# Documentation
#--------------
#
# This script is used to generate all the data

# Moving to game folder
cd ../src/

# Generating data on the different maps
#
# MAP 1
for((i = 1 ; i <= 1 ; i++))
do
        python3 run.py --agentfile PacMAN.py --ghostagent dumby  --generate 1 --layout world_2 --silentdisplay
        clear
        python3 run.py --agentfile PacMAN.py --ghostagent greedy --generate 1 --layout world_2 --silentdisplay
        clear
        python3 run.py --agentfile PacMAN.py --ghostagent smarty --generate 1 --layout world_2 --silentdisplay
        clear
done




