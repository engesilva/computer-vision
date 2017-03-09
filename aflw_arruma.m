clear all;
close all;
path = '/home/fhenrique/';

all = fopen(strcat(path,'all.csv'));

P = textscan(all, '%s','delimiter', '\n');
P = P{1};

h = fopen(strcat(path,'finall.csv'),'w');

[l,c] = size(P);

tic;
for i=1:l

    a = P{i};
    
    line = fopen(strcat(path,a));
    
    Pa = textscan(line, '%s','delimiter', '\n');
    c1 = strjoin(Pa{1}(1));
    c2 = strjoin(Pa{1}(2));
     
   
    str = strcat([c1,' ','1',' ',c2,'\n']);
    fprintf(h,str);
   

end
fclose('all');
toc;
