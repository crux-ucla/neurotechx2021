%{

This is a temporary program until the P300 data gathering program is
configured to automatically/continually save trial data. It expects the
existence a folder "Crux_Trial_Data" in the working directory and for the
trial data (stimCodes and potential) to be active in the MATLAB workspace.

CruX UCLA Fall 2021
Darren Vawter

%}

i = 0;
file = "";

while true
    file = "CruX_trial_data/trial";
    file = strcat(file,num2str(i,'%d'));
    file = strcat(file,".mat");
    if(isfile(file))
        i = i+1;
    else
        break
    end
end

save(file,'stimCodes','potential')