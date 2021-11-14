# Setup OpenBCI Lab Streaming Layer (LSL) to work with MATLAB:

### You will need MATLAB or MATLAB online.
-I have only ensured that it works with MATLAB R2021B desktop edition
-you should have access to it for free through UCLA

### Step 1: install the libsls-Matlab folder from this repo **only**
-you do not need to install libLSL from the OpenBCI repo
	
### Step 2: download BCI Competition III problem IIB P300 data
-I have uploaded this data to the club's google drive
-alternatively, it is publicly available from the BCI Competition website (account necessary)
	-(if you get the data from the website, you will need to rename the folder)
	
### Step 3: move the data inside of the following directory:
*...\liblsl-Matlab\_EEG_scripts\Stream_Visualization*
	 
### Step 4: ensure matlab has an internal C/C++ compiler linked for building MEX files
-check by running the following command in the MATLAB command line:
	 *mex.getCompilerConfigurations('C','Selected')*
-if nothing is returned, or you receive an error, install MinGW-w64:
	-in Matlab --> in the Home tab --> in the Environment section:
	-click Add-Ons --> Get Add-Ons
	-search for MinGw and install it
-I have only ensured that it works with MinGW-w64

### Step 5: build the MEX files
-open MATLAB
-navigate to the directory where you have installed the liblsl-Matlab folder
-right click liblsl-Matlab
	-click Add To Path --> Selected Folder and Subfolders
-navigate inside of liblsl-Matlab folder
-once inside, use the MATLAB command line and run:
	 *build_mex*

### At this point, LSL should be setup to work with MATLAB.

# LSL Stream simulation and visualization:

### Step 1: open two separate instances of MATLAB

### Step 2: add files to the MATLAB path (in BOTH instances of MATLAB)
-navigate to the directory where you have installed the liblsl-Matlab folder
-right click liblsl-Matlab
	-click Add To Path --> Selected Folder and Subfolders

### Step 3: in both instances, naviagate inside of:
 *...\liblsl-Matlab\_EEG_scripts\Stream_Visualization*

### Step 4: in one instance, open and run *Simulate_Stream_BCI_Comp_III_IIB*
-alternatively, you can simulate random normal numbers by opening:
	*Simulate_Stream_Random*
-read the short commentary at the top of the script to understand what is being done

### Step 5: in the other instance, open and run *Plot_Stream_Data*
-read the commentary at the top of the script as you may want to change some variables

### At this point, the first instance should be streaming data through OpenBCI's LSL and the second should be displaying it.
### To close the programs, ***FIRST*** stop *Plot_Stream_Data*, ***THEN*** stop *Simulate_Stream_BCI_Comp_III_IIB*
