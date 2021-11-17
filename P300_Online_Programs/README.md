# Online P300 Programs

This directory contains all of the necessary programs to perform P300 trials with the OpenBCI cap. It is assumed that MATLAB LSL interface is setup and Python LSL interface is setup; they are required.

This commit contains sloppy code is not appropriately commented in som places. It is commited solely for the purpose of ensuring that the team has a working copy of the code on the GITHUB repo.

#### Step 1: Connect the OpenBCI cap, launch the OpenBCI gui, and start a data stream

#### Step 2: In the OpenBCI GUI, open "Networking" in one of the windows
	-Change the type from serial to LSL in the top right of this window.
	-Create and start a time-series EEG stream in the far left dropdown box.
	-(do not change the default name *openbci_eeg1*...or whatever it is)

#### Step 3: Launch the MATLAB script, *P300_Data_Gatherer.m*
	-The message *Resolving an EEG stream...* should now display and PASS.
	-If it hangs, then it was unable to resolve/find the OpenBCI LSL stream.
	-It should hang on *Resolving stimuli stream...* (this is intentional).

#### Step 4: Launch the Python program *P300_GUI_and_Stimuli.py*
	-(On the first attempt, you may want to ensure that the data gatherer resolved this stimuli stream and is now receiving data, then restart from step 3).
	-At this point, the P300 GUI should display, and the user wearing the OpenBCI cap can perform the trials.

#### Step 5: When the trial is complete, immediately shut down the MATLAB script *P300_Data_Gatherer.m*
	-This will prevent the data gatherer from gathering too much data and potentially overwriting good data.

#### Step 6: In the same MATLAB workspace, run *Save_P300_Trial.m*
	-This program expects the folder *Crux_trial_data* to be in the same directory.
	-This will permanently save the trial data to your drive.

#### Step 7: Close *P300_GUI_and_Stimuli.py* and disconnect OpenBCI
