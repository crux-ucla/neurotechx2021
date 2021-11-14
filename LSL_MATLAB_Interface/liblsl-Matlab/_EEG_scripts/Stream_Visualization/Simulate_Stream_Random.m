%{

This code streams 8 simulated channels of incoming EEG data by using
numbers randomly sampled from a normal distribution ~N(0,1).

The OpenBCI headset samples data at 125 Hz, so this stream outputs data at
the same frequency.

CruX UCLA Fall 2021
Darren Vawter

%}

%% instantiate the LSL library
disp('Loading library...');
lib = lsl_loadlib();

% make a new stream outlet
disp('Creating a new streaminfo...');
info = lsl_streaminfo(lib,'BioSemi','EEG',8,100,'cf_float32','sdfwerr32432');

disp('Opening an outlet...');
outlet = lsl_outlet(info);

% send data into the outlet, sample by sample
disp('Now transmitting data...');
while true
    outlet.push_sample(randn(8,1));
    pause(1/125);
end