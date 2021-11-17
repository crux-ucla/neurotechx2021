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