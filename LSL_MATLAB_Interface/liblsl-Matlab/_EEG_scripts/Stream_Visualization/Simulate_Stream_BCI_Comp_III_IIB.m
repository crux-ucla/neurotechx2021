%{

This code streams 8 simulated channels of incoming EEG data by using the
BCI-Competition-III problem-II_B's publicly available P300 dataset.

The BCI-Competition-III problem-II_B's data is sampled at 240 Hz, so this
stream outputs data at the same frequency.

CruX UCLA Fall 2021
Darren Vawter

%}

%% load the EEG data to stream
load 'BCI_Comp_III_IIB_Data/Subject_A_Train.mat';
    % convert to double precision
Signal=double(Signal);
Flashing=double(Flashing);
StimulusCode=double(StimulusCode);
StimulusType=double(StimulusType);

%% select 8 channels that have comparable positions on the OpenBCI Cap
%{
    C=central, P=parietal, O=occipital
    18  --> CP(z)   --> channel 1
    48  --> P(3)    --> channel 2
    51  --> P(z)    --> channel 3
    54  --> P(4)    --> channel 4
    56  --> PO(7)   --> channel 5
    60  --> PO(8)   --> channel 6
    61  --> O(1)    --> channel 7
    63  --> O(2)    --> channel 8
%}
channels = [18,48,51,54,56,60,61,63];

%re-assign signal to have only these channels
Signal = Signal(:,:,channels);

%% load the LSL library
disp('Loading library...');
lib = lsl_loadlib();

%% create and open a new stream outlet
disp('Creating a new streaminfo...');
info = lsl_streaminfo(lib,'simulation','EEG',8,100,'cf_float32','sdfwerr32432');

disp('Opening an outlet...');
outlet = lsl_outlet(info);

%% repeatedly send data into the outlet, sample by sample @240Hz
disp('Now transmitting data...');
% this will repeat the data set over and over
while true
    % stream each epoch (end-to-end) (32.475 seconds of data per epoch)
    for epoch = 1:85
        % stream each sample (wait 1/240 seconds between each output)
        for sample = 1:7794
            % stream each channel simultaneously
            outlet.push_sample(Signal(epoch,sample,:));

            % simulate the time between samples (sampling @240Hz)
            pause(1/240)
        end
    end
end