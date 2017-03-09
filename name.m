clear all;
close all;
path = '/home/fhenrique/base_3dafw/male/valid_lm/';
all = fopen(strcat(path,'all.txt'));

P = textscan(all, '%s','delimiter', '\n');
P = P{1};

[l,c] = size(P);

tic;
for i=1:l

    a = P{i};
    
    cmd = strcat(['cp ',path,a,' ',path,a(1:end-7),a(end-3:end)]);

    dos (cmd);
   

end
fclose('all');
toc;
