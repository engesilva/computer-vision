clear all;
close all;
path = '/home/fhenrique/experiments/gender/aflw/files/';

a = fopen(strcat(path,'gender_labels_correct_path.txt'));

P = textscan(a, '%s','delimiter', '\n');
P = P{1};

b = fopen(strcat(path,'nose.txt'));

G = textscan(b, '%s','delimiter', '\n');
G = G{1};

h = fopen(strcat(path,'saida_aflw.csv'),'w');

[l,c] = size(P);

[l1,c1] = size(G);

tic;
for i=1:l

    a = P{i}; 
    F1 = textscan(a, '%s','delimiter', ' ');
    F1 = F1{1};
    
    for j=1:l1
        b = G{j};
        F2 = textscan(b, '%s','delimiter', ' ');
        F2 = F2{1};
        if strcmp(F1{1},F2{1})
            fprintf(h,strcat(a,'\n'));
            break;
        end
    end
    
   
end
fclose('all');
toc;
