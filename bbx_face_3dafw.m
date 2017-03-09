clear all;
close all;
path = '/home/fhsilva/3dafw/valid_bb/';
path2 = '/public/bases/3dafw/valid_img/';
all = fopen(strcat(path,'all.txt'));

P = textscan(all, '%s','delimiter', '\n');
P = P{1};

h = fopen(strcat(path,'saida_valid.txt'),'w');

[l,c] = size(P);

tic;
for i=1:l

    a = P{i};
    
    file = fopen(strcat(path,a));
    F = textscan(file, '%s','delimiter', ',');
    F = F{1};
 
    
    str = strcat([path2, a(1:end-4),'.jpg', ' 1 ',F{1},' ', F{2},' ',F{3},' ',F{4},'\n']);
    fprintf(h,str);
   

end
fclose('all');
toc;
