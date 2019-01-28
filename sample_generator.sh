#!/bin/bash

# Anni Xiong
# This is to generate MG events with parameters specified
# has to be in same directory as Mad Graph Cards
# The whited out param_0default.dat has to be present in the current directory

#----------------------- parameters
g="2.1"
y1w="42640"  #total z prime decay width
y1m="20000" #Zprime mass

gaxd="1"    # axial coupling to one kind of the DM particle
Xdm="10"    # mass of the corresponding DM particle

#------------------------ subject to change

cd ./Cards

# White out the revised param_card
rm param_card.dat
cp -pi "param_0default.dat" "param_card.dat"

#Editting the param card
sed "s/ 0.000000e+00 # gAXd/ ${gaxd} # gAXd/g" param_card.dat > param_card2.dat

sed "s/ 0.000000e+00 # gAd11/ ${g} # gAd11/g" param_card2.dat  >param_card3.dat
sed "s/ 0.000000e+00 # gAu11/ ${g} # gAd11/g" param_card3.dat  >param_card4.dat
sed "s/ 0.000000e+00 # gAd22/ ${g} # gAd22/g" param_card4.dat  >param_card5.dat
sed "s/ 0.000000e+00 # gAu22/ ${g} # gAu22/g" param_card5.dat  >param_card6.dat
sed "s/ 0.000000e+00 # gAd33/ ${g} # gAd33/g" param_card6.dat  >param_card7.dat
sed "s/ 0.000000e+00 # gAu33/ ${g} # gAd33/g" param_card7.dat  >param_card8.dat

sed "s/ 1.000000e+03 # MY1/ ${y1m} # MY1/g" param_card8.dat >param_card9.dat
sed "s/ 1.000000e+01 # MXd/ ${Xdm} # MXd/g" param_card9.dat >param_card10.dat

sed "s/ 1.000000e+01 # WY1/ ${y1w} # WY1/g" param_card10.dat >param_card11.dat

if [ $? -eq 0 ]  #check execution status
then
	rm param_card[2-9].dat
	rm param_card10.dat
	rm param_card.dat 
	mv param_card11.dat  param_card.dat
	echo "param_card is successfully edited"
	sleep 5s
	cd ..
	./bin/generate_events y1_20_200 -f      	  # Generate events with specified name, use default answers
	cd ./Events/y1_20_200
	gunzip unweighted_events.lhe.gz
	mv ./unweighted_events.lhe ./y1_20_200.lhe    # name change
else 
	echo "param_card not edited"

fi


# make changes for the lhe file input directory in Pythia_LHEinput.cmd at
# /afs/cern.ch/work/a/axiong/public/FCCsoft/FCCSW/Generation/data
# go back to FCCSW main directory
# cd /afs/cern.ch/work/a/axiong/public/FCCsoft/FCCSW
# Add showering and generate root file with Pythia
#./run fccrun.py Sim/SimDelphesInterface/options/PythiaDelphes_config.py --inputfile=Generation/data/Pythia_LHEinput.cmd --outputfile=pp_y1_20_025.root --delphescard=delphes_card/card.tcl --nevents=5000

#if [ $? -eq 0 ]
#then
	# go to heppy
	# cd ./FCChhAnalyses/pp_Zprime
	# Make changes in analysis.py to tell heppy location of the root file generated in last dtep.
	# run heppy command
	# heppy_loop.py out_35000_100000/ analysis.py
#fi

# Finally run the hist.py to produce histograms
