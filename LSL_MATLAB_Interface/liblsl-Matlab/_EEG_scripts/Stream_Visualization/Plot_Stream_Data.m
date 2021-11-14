%{

This code plots 8 channels of incoming LSL stream data on a single plot in
a color-coded manner comparable to the OpenBCI GUI.

If you are using OpenBCI/BCI_Comp/other data, ensure matching of:
    samplingFreq  --> the sampling frequency of the incoming stream
If you want to plot more data going back in time change:
    secondsToPlot --> the number of seconds worth of data to store and plot
If the plot is drawing too slowly, increase:
    drawEfficiancy--> inverse of frame rate cap (depends on PC capability)
If you want to change the chanel labels, change:
   channelLabel   --> array of channel names displayed on the plot

CruX UCLA Fall 2021
Darren Vawter

%}

%% instantiate the LSL library
disp('Loading the library...');
lib = lsl_loadlib();

%% resolve an LSL stream by looping infinitely until one is returned
disp('Resolving an LSL stream...');
result = {};
while isempty(result)

    % load the LSL stream by property
    % if 'type' is chosen as property:
    % ensure that you are not streaming simulated EEG data at the same time
    % (bc the stream will simply be whichever one broadcasts first) 
    
    % IF USING LIVE DATA, UNCOMMENT THE ASSIGNMENT BELOW
    % (ensure name matches stream if the default name was changed)
    % result = lsl_resolve_byprop(lib,'name','obci_eeg1'); end
    
    % IF USING SIMULATED DATA, UNCOMMENT THE ASSIGNMENT BELOW
    result = lsl_resolve_byprop(lib,'type','EEG');
end

%% initialize values

% average sampling frequency of incoming samples
%   openBCI EEG     -->     125 Hz
%   BCI comp data   -->     240 Hz
samplingFreq = 240;

% number of elapsed seconds to show on the plot
secondsToPlot = 5;

% channel alignments: TBD (when we decide what channels to use and where)
channelLabel = ["Ch 1","Ch 2","Ch 3","Ch 4","Ch 5","Ch 6","Ch 7","Ch 8",];

% this controls how frequently the program redraws the plot
% (it's basically the inverse of your framerate: lower ==> higher fps cap)
% you may need to increase this number if the plot appears to be draw slow
% minimum value is 1 (redraw after every single sample)
drawEfficiancy = 25;

% number of samples to hold in RAM
samplesToHold = secondsToPlot*samplingFreq;

% invert secondsToPlot for negative (elapsed time) plotting
secondsToPlot = -secondsToPlot;

% (samplesToHold)x(8) matrix of potential values (samplesToHold samples across 8 channels)
potential = zeros(samplesToHold,8);

% (samplesToHold)x(1) array of timestamps (time[X] is the timestamp for potential[X,i]
time = zeros(samplesToHold,1);

% this tracks the current index for both <potentials> and <time>
% it is incremented for each sample that we recieve
index = 1;

% timestamp of the last sample (helpful for plotting time backwards)
% this is used for comparing time between samples which *should* be the
% same if our sampler is consistent, BUT the simulated data is not
% constantly sampled AND our sampler may fault at times
last = 0;

% colors for plotting
% (matched to default channel colors of openBCI)
color=["#696969","#9900CC","#0033BB","#009900","#EEEE00","#FF7500","red","#B65B00",];

% mininmum and maximum potentials (used as lazy auto-resolution of plots)
min = zeros(8,1);
max = ones(8,1);
% plot level of each electrode (vertical shift so they don't overlap)
level = [0,1,2,3,4,5,6,7];

%draw all potentials on the same plot
subplot(1,1,1);

%% create a new inlet from the LSL stream data (i.e. ignore other metadata)
disp('Opening an inlet...');
inlet = lsl_inlet(result{1});

%% act on data stream indefinitely
disp('Now receiving data...');

while true

    % get data from the inlet
    %   vec --> raw 8x1 array of channel potentials
    %   ts  --> timestamp that the data was transmitted at
    [vec,ts] = inlet.pull_sample();

    %check if channel plot needs to be rescaled
    for ch = 1:8
        % if the max/min height is not high/low enough, fix it
        if(vec(ch) > max(ch))
            max(ch) = vec(ch);
            %update plot levels
            for chh = ch+1:8
                level(chh) = level(chh-1) + max(chh-1) - min(chh);
            end
        elseif(vec(ch) < min(ch))
            min(ch) = vec(ch);
            %update plot levels
            if(ch==1)
                level(ch) = min(ch);
            end
            for chh = ch+1:8
                level(chh) = level(chh-1) + max(chh-1) - min(chh);
            end
        end
    end

    % get potentials at the current stamp index
    potential(index,:) = vec;

    % calculate time delta between this sample and the last one
    tD = ts-last;

    % set this timestamp as the 'last' timestamp for the next sample
    last = ts;
    
    % set the current time stamp to 0
    % this is because we plot time as: seconds from current time
    time(index) = 0;
    
    % subtract the elapsed time since last sample from all other timestamps
    %   all indices before the current index
    time(1:index-1) = time(1:index-1)-tD;
    %   all indices after the current index
    time(index+1:samplesToHold) = time(index+1:samplesToHold)-tD;

    % redraw the plots every drawEfficiency samples (less drawing=faster) 
    if mod(index,drawEfficiancy)==0
        % turn hold off so the next redraw erases this one
        hold off;

        % for each electrode
        for electrode=1:8
            % plot all the values up to, and including, the current index
            plot(time(1:index),potential(1:index,electrode)+level(electrode)-min(1),'Color',color(electrode));
            % turn hold on to concatenate the two plots end-to-end
            hold on;
            % plot all the values after the current index
            plot(time(index+1:samplesToHold),potential(index+1:samplesToHold,electrode)+level(electrode)-min(1),'Color',color(electrode));
        end
        
        % time axis is always X seconds ago to present (0 seconds ago)
        % potential depends on global min/max potential sum
        axis([secondsToPlot 0 min(1) level(8) + max(8) - min(8)]);
        
        % plot title
        title("EEG potentials")

        % x axis label
        xlabel("time elapsed (s)")

        % y axis tick labels
        yticklabels(channelLabel);

        % y axis tick values
        yticks(level'+max);

        % immediately draw the plots (don't wait for the program to finish)
        drawnow;
    end

    % increment the channel index
    index = index + 1;
    % if the channel index is at the end of the array, return to the
    % beginning (to retrace over old values)
    if index > samplesToHold
        index = 1;
    end

end




