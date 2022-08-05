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

clear

# Moving to game folder
cd ../src/

# Terminal UI (1)
echo "\n"
echo "__________________        ____________________________________________"
echo "                  |      |                                            "
echo "                  |      |                                            "
echo "     PacNET       |      |          Victor Mangeleer  -  2022         "
echo "                  |      |                                            "
echo "__________________|      |____________________________________________"
echo "     ,--.    ,--.          ,--.   ,--."
echo "    |oo  | _  \   .       | oo | |  oo|"
echo "o  o|~~  |(_) /   ;       | ~~ | |  ~~|o  o  o  o  o  o  o  o  o  o  o"
echo "    |/\/\|   '._,'        |/\/\| |/\/\|"
echo "__________________        ____________________________________________"
echo "                  |      |"
echo "__________________|      |____________________________________________"
echo "\n"
echo "------"
echo " Data"
echo "------\n"
echo " Currently generating the data..."
echo "\n"

#
# Generating data on the different maps
#
# MAP 1
for((i = 1 ; i <= 30 ; i++))
do
        python3 run.py --agentfile PacMAN.py --ghostagent dumby  --generate 1 --layout map_1 --silentdisplay
        python3 run.py --agentfile PacMAN.py --ghostagent greedy --generate 1 --layout map_1 --silentdisplay
        python3 run.py --agentfile PacMAN.py --ghostagent smarty --generate 1 --layout map_1 --silentdisplay
done


# Terminal UI (2)
clear
echo "\n"
echo "__________________        ____________________________________________"
echo "                  |      |                                            "
echo "                  |      |                                            "
echo "     PacNET       |      |          Victor Mangeleer  -  2022         "
echo "                  |      |                                            "
echo "__________________|      |____________________________________________"
echo "     ,--.    ,--.          ,--.   ,--."
echo "    |oo  | _  \   .       | oo | |  oo|"
echo "o  o|~~  |(_) /   ;       | ~~ | |  ~~|o  o  o  o  o  o  o  o  o  o  o"
echo "    |/\/\|   '._,'        |/\/\| |/\/\|"
echo "__________________        ____________________________________________"
echo "                  |      |"
echo "__________________|      |____________________________________________"
echo "\n"
echo "------"
echo " Data"
echo "------\n"
echo " Done"
echo "\n"