% clc
% clear all
% close all
list = glob('./*.png');
for i=1:length(list)
   img{i} = imread(list{i}); 
end

load roi;
for i=1:length(roi)
    data(i,:) = roi(i).objectBoundingBoxes;
end