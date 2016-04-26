% #---------------------------------------------------------------------------------------------------
% # This code is used for assist the use of distance-based group contribution (DBGC) method.
% # The code is published under the MIT open source license.
% 
% # The MIT License (MIT)
% # Copyright (c) 2016 by the DBGC Team (DBGConline@gmail.com)
% 
% # Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
% # and associated documentation files (the "Software"), to deal in the Software without restriction, 
% # including without limitation the rights to use, copy, modify, merge, publish, distribute, 
% # sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
% # furnished to do so, subject to the following conditions:
% 
% # The above copyright notice and this permission notice shall be included in all copies or 
% # substantial portions of the Software.
% 
% # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
% # BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
% # NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
% # DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
% # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
% #---------------------------------------------------------------------------------------------------
% 
%
% This file is used for prediction with group contribution vectors.
%
% The input file should be put in the directory DBGCVectors, Then the group contribution vectors in the file like 
% DBGCVectors\DBGCVectors.xlsx will be imported. This code will import the trained net like 
% savedNet\parameterizedAlgorithm.mat and prediction the standard enthalpy of formation of the species in DBGCVectors.xlsx.
% 
% The output will be displayed in the MATLAB output window, which is the variable predicted_test_Y.
%

close all;
clear;
clc;

inputStartLine = 4;
outputStartLine = 4;
sampleSize = xlsread('DBGCVectors\DBGCVectors.xlsx','inputVectors','B2:B2');

inputData = xlsread('DBGCVectors\DBGCVectors.xlsx','inputVectors',['F' num2str(inputStartLine) ':FS' num2str(inputStartLine+sampleSize-1)]);    % 所有样本

[~,speciesName,~] = xlsread('DBGCVectors\DBGCVectors.xlsx','inputVectors',['FV' num2str(outputStartLine) ':FV' num2str(outputStartLine+sampleSize-1)]);

test_X = inputData;
test_speciesName = speciesName;

vectorDimension=size(test_X,2);
tmp_num=solve(subs('N*(N+3)/2=vectorDimension'),'N');
regressionTruncate = tmp_num(find(tmp_num>0));

load(['savedNet\parameterizedAlgorithm'])

predicted_test_Y = trained_ANN_net(test_X(:,regressionTruncate+1:end)');    
predicted_test_Y = predicted_test_Y';
predicted_test_Y = predicted_test_Y + [ones(size(test_X,1),1),test_X(:,[1:regressionTruncate])]*reg_coeff

% for i=inputStartLine:inputStartLine+sampleSize-1
%     xlswrite('DBGCVectors\DBGCVectors.xlsx',predicted_test_Y,'inputVectors',['FW' num2str(inputStartLine) ':FW' num2str(inputStartLine+sampleSize-1)]);
% end




