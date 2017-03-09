clear all;
close all;
path = '/home/fhenrique/experiments/gender/ijba/';

a = fopen(strcat(path,'gender.txt'));

P = textscan(a, '%s','delimiter', '\n');
P = P{1};

h = fopen(strcat(path,'ijba.txt'),'w');

[l,c] = size(P);

tic;
for i=2:l

    a = P{i};
   
    F1 = textscan(a, '%s','delimiter', ' ');
    F1 = F1{1};    
    if str2num(F1{7})==1
       fprintf(h,strcat([F1{1},' ', F1{2},' ',F1{3},' ',F1{4},' ',F1{5},' ',F1{6},'\n']));
    end
   
end
fclose('all');
toc;

