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
% This file is used for training and test.
%
% The input file should be put in the directory dataBase, Then the data in the file like 
% dataBase\inputFile_m.xlsx will be imported. Then according to the configuration, the training set 
% and test set will be generated for later training and test.
% 
% The output file is the trained net for further prediction, which is stored as savedNet\parameterizedAlgorithm.mat.
% The figures and error statistics will also be save in the directories Figure or Error.
%
% Tips:
% The random seed is set for reproducibility. Current seed is selected to be able to give a relatively good 
% prediction on the training set, test set and the experimental data we can find. A change of the seed would 
% affect the prediction for every single species, but the overall statistic behavior will be hold stable. 
% So it is pointless to only care about only very few cases. It is more meaningful to evaluate the method 
% with the statistic result for a large amount of species. A simple statistic will be given during each 
% process of training and test.
% 
% Generally, the variable regressionTruncate equals to N, and the dimension of the group contribution vector is 
% N*(N+3)/2. However, if the group contribution vector is not directly generated by the code provided, the number 
% of regressionTruncate should be adjusted to represent the number of types of individual groups.   
% 

close all;
clear;
clc;
% rand('state',0);
rng(295);


% obtain the data
testC = {'C12','C13'};            % the species in the test set
trainC = {'C3','C4','C5','C6','C7','C8','C9','C10','C11'};    %the species in the training set

testClass = 2;      % 0: test alkyl and akenyl radicals 1: test alkene 2: test alkane
trainClass = 0;      % 0: train alkane, alkene and radicals 1: train alkane only

testC_Num = length(testC);
trainC_Num = length(trainC);

inputStartLine = 4;
outputStartLine = 4;

trainSize = 5000; 

saveFlag = 1;        % 0: don't save figure and table 1: save figure and table

hiddenLayerValue = 10;    % number of neurons in the hidden layer
transferFcnName = 'logsig';  % logsig [0 1], tansig [-1 1]


testMeanError = 0;   % mean unsigned error on test set
trainMeanError = 0;   % mean unsigned error on train set


sampleSize = 20000;
testSampleSize = 300;   
inputData = xlsread('dataBase\inputFile_m.xlsx','acyclic',['F' num2str(inputStartLine) ':FS' num2str(inputStartLine+sampleSize-1)]);    % 所有样本
outputData = xlsread('dataBase\inputFile_m.xlsx','acyclic',['FW' num2str(outputStartLine) ':FW' num2str(outputStartLine+sampleSize-1)]);  % 所有样本
[~,speciesName,~] = xlsread('dataBase\inputFile_m.xlsx','acyclic',['FV' num2str(outputStartLine) ':FV' num2str(outputStartLine+sampleSize-1)]);    

sampleSize = length(outputData);

% classification of samples in test set
if(testClass == 1)
	% only alkene in test set
	C_Test_Index=[];
	C_Test_IndexCyclic=[];
	C_Train_IndexCyclic=[];
	for testIndex = 1:testC_Num
		speciesPreName = testC{testIndex};
		speciesPreNameLength = length(speciesPreName);
		C_Num = str2num(speciesPreName(2:speciesPreNameLength));
		H_Num = C_Num*2;

		testNamePattern = ['^' speciesPreName 'H' num2str(H_Num) '_+[0-9]+$'];
		testMatch = regexp(speciesName,testNamePattern);
		Temp_C_Test_Index = find(cellfun(@(x) length(x)>0, testMatch));
		C_Test_Index=[C_Test_Index;Temp_C_Test_Index]
	end
elseif(testClass == 2)
	  % only alkane in test set
	C_Test_Index=[];
	C_Test_IndexCyclic=[];
	C_Train_IndexCyclic=[];
	for testIndex = 1:testC_Num
		speciesPreName = testC{testIndex};
		speciesPreNameLength = length(speciesPreName);
		C_Num = str2num(speciesPreName(2:speciesPreNameLength));
		H_Num = C_Num*2+2;

		testNamePattern = ['^' speciesPreName 'H' num2str(H_Num) '_+[0-9]+$'];
		testMatch = regexp(speciesName,testNamePattern);
		Temp_C_Test_Index = find(cellfun(@(x) length(x)>0, testMatch));                
		C_Test_Index=[C_Test_Index;Temp_C_Test_Index];
    end
elseif(testClass == 0)
	C_Test_Index=[];
	C_Test_IndexCyclic=[];
	C_Train_IndexCyclic=[];
	tmp_countAlkane = 0;
	tmp_countAlkene = 0;
	for testIndex = 1:testC_Num  
		speciesPreName = testC{testIndex};
		speciesPreNameLength = length(speciesPreName);
		C_Num = str2num(speciesPreName(2:speciesPreNameLength));
		H_Num = C_Num*2+2;
		if C_Num >= 10
			testNamePattern = ['^' speciesPreName 'H' num2str(H_Num) '_+[0-9]+_r[0-9]+.*$'];
			testMatch = regexp(speciesName,testNamePattern);
			Temp_C_Test_Index = find(cellfun(@(x) length(x)>0, testMatch));                
			C_Test_Index=[C_Test_Index;Temp_C_Test_Index];
			tmp_countAlkane = tmp_countAlkane +length(Temp_C_Test_Index);
		end
		
		speciesPreName = testC{testIndex};
		speciesPreNameLength = length(speciesPreName);
		C_Num = str2num(speciesPreName(2:speciesPreNameLength));
		H_Num = C_Num*2;
		if C_Num >= 9
			testNamePattern = ['^' speciesPreName 'H' num2str(H_Num) '_+[0-9]+_r[0-9]+.*$'];
			testMatch = regexp(speciesName,testNamePattern);
			Temp_C_Test_Index = find(cellfun(@(x) length(x)>0, testMatch));                
			C_Test_Index=[C_Test_Index;Temp_C_Test_Index];
			tmp_countAlkene = tmp_countAlkene +length(Temp_C_Test_Index) ;
		end          
	end
	tmp_countAlkane;
	tmp_countAlkene;
else
	mgmox(['Error value of testClass']);
end

% classification of samples in training set
if(trainClass == 1)
	  % only alkane in training set
	Train_Index=[];
	for trainIndex = 1:trainC_Num
		speciesPreName = trainC{trainIndex};
		speciesPreNameLength = length(speciesPreName);
		C_Num = str2num(speciesPreName(2:speciesPreNameLength));
		H_Num = C_Num*2+2;

		testNamePattern = ['^' speciesPreName 'H' num2str(H_Num) '_+[0-9]+$'];
		testMatch = regexp(speciesName,testNamePattern);
		Temp_C_Train_Index = find(cellfun(@(x) length(x)>0, testMatch));    
		Train_Index=[Train_Index;Temp_C_Train_Index];            
    end
elseif(trainClass == 0)
	  % alkane, alkene, alkyl and alkenyl radical in training set
	Train_Index=[];
	for trainIndex = 1:trainC_Num
		speciesPreName = trainC{trainIndex};
		speciesPreNameLength = length(speciesPreName);
		C_Num = str2num(speciesPreName(2:speciesPreNameLength));
		H_Num = C_Num*2+2;
		trainSpeciesPreName = [speciesPreName 'H' num2str(H_Num)];
		trainSpeciesPreNameLength = length(trainSpeciesPreName);
		Temp_C_Train_Index = find(strncmp(speciesName,trainSpeciesPreName,trainSpeciesPreNameLength));
		
		if C_Num < 10
			testNamePattern = ['^' speciesPreName 'H' num2str(H_Num) '_+[0-9]+.*$'];
		elseif C_Num >= 10
			testNamePattern = ['^' speciesPreName 'H' num2str(H_Num) '_+[0-9]+$'];
		end
		testMatch = regexp(speciesName,testNamePattern);
		Temp_C_Train_Index = find(cellfun(@(x) length(x)>0, testMatch));    
		
		Train_Index=[Train_Index;Temp_C_Train_Index];            
	end
	tmp_trainC = {'C3','C4','C5','C6','C7','C8'};
	for trainIndex = 1:length(tmp_trainC)
		speciesPreName = tmp_trainC{trainIndex};
		speciesPreNameLength = length(speciesPreName);
		C_Num = str2num(speciesPreName(2:speciesPreNameLength));
		H_Num = C_Num*2;
		trainSpeciesPreName = [speciesPreName 'H' num2str(H_Num)];
		trainSpeciesPreNameLength = length(trainSpeciesPreName);
		Temp_C_Train_Index = find(strncmp(speciesName,trainSpeciesPreName,trainSpeciesPreNameLength));
		Train_Index=[Train_Index;Temp_C_Train_Index];            
	end        
else
	mgmox(['Error value of testClass']);
end

train_X  = inputData(Train_Index,:);
train_Y = outputData(Train_Index,:);
train_speciesName  = speciesName(Train_Index,:);

trainingSampleSize = size(train_Y,1);
if trainSize>trainingSampleSize
	trainSize = trainingSampleSize;
	msgbox(['trainSize cannnot larger than ' num2str(trainingSampleSize)]);
end

randIndex = randperm(trainingSampleSize,trainSize);

train_X = train_X(randIndex,:);
train_Y = train_Y(randIndex,:);
train_speciesName  = train_speciesName(randIndex,:);

test_X = inputData(C_Test_Index,:);
test_Y = outputData(C_Test_Index,:);
test_speciesName = speciesName(C_Test_Index);
C_Test_IndexSize = length(C_Test_Index);

testSampleSize = length(test_Y);

vectorDimension=size(train_X,2);
tmp_num=solve(subs('N*(N+3)/2=vectorDimension'),'N');
regressionTruncate = tmp_num(find(tmp_num>0));

% regression
[reg_coeff reg_coeffint reg_resid reg_residint reg_stats]=regress(train_Y, [ones(size(train_X,1),1),train_X(:,[1:regressionTruncate])]);
train_Y_regress = [ones(size(train_X,1),1),train_X(:,[1:regressionTruncate])]*reg_coeff;
train_Y = train_Y - train_Y_regress;


ANN_net = fitnet(hiddenLayerValue);
ANN_net.trainFcn='trainlm';         % trainlm, trainscg
ANN_net.performFcn='mse';
ANN_net.layers{1}.transferFcn = transferFcnName;  % logsig [0 1], tansig [-1 1]
ANN_net.layers{2}.transferFcn = 'purelin';  % purelin
ANN_net.divideParam.trainRatio = 80/100;
ANN_net.divideParam.valRatio = 10/100;
ANN_net.divideParam.testRatio = 10/100;
ANN_net.trainParam.goal = 1e-8;
ANN_net.trainParam.min_grad = 1e-10;
ANN_net.trainParam.showWindow = 1;
ANN_net.trainParam.epochs = 100;
ANN_net.trainParam.max_fail = 10;


% training
[trained_ANN_net,~]=train(ANN_net,train_X(:,regressionTruncate+1:end)',train_Y');
% save the net
save('savedNet\parameterizedAlgorithm', 'trained_ANN_net', 'reg_coeff');

predicted_test_Y = trained_ANN_net(test_X(:,regressionTruncate+1:end)');   
predicted_test_Y = predicted_test_Y';
predicted_train_Y = trained_ANN_net(train_X(:,regressionTruncate+1:end)'); 
predicted_train_Y = predicted_train_Y';

predicted_test_Y = predicted_test_Y + [ones(size(test_X,1),1),test_X(:,[1:regressionTruncate])]*reg_coeff;
predicted_train_Y = predicted_train_Y + train_Y_regress;
train_Y = train_Y + train_Y_regress;



% error statistics
%  R^2 
R_square_test_samples = 1 - sum((test_Y-predicted_test_Y).^2) / sum((test_Y-mean(test_Y)).^2)
R_square_train_samples = 1 - sum((train_Y-predicted_train_Y).^2) / sum((train_Y-mean(train_Y)).^2)

% deviation
A_error_test_samples = test_Y-predicted_test_Y;
A_error_train_samples = train_Y-predicted_train_Y;
Ratio_less_1_test_samples = (length(find(abs(A_error_test_samples)<=1)) / testSampleSize)*100;
Ratio_less_2_test_samples = (length(find(abs(A_error_test_samples)<=2)) / testSampleSize)*100;
Ratio_less_1_train_samples = (length(find(abs(A_error_train_samples)<=1)) / trainSize)*100;
Ratio_less_2_train_samples = (length(find(abs(A_error_train_samples)<=2)) / trainSize)*100;
testMeanError = mean(abs(A_error_test_samples));
trainMeanError = mean(abs(A_error_train_samples));

% output the deviation into files
if(~isdir('Error'))
    mkdir('Error');
end
delete('Error\Sorted_error_test_samplesValue.xlsx');
delete('Error\Sorted_error_train_samplesValue.xlsx');

[error_test_samplesValue, error_test_samplesIndex] = sort(abs(A_error_test_samples),'descend');
cell_error_test_samplesValue = [test_speciesName(error_test_samplesIndex) num2cell(A_error_test_samples(error_test_samplesIndex))];
cell_error_samplesValue_Title={'SpeciesName','Error','Mean Error'};
if saveFlag == 1
    save('Error\A_error_test_samples.txt','-ascii','A_error_test_samples');
    save('Error\A_error_train_samples.txt','-ascii','A_error_train_samples');
    xlswrite('Error\Sorted_error_test_samplesValue.xlsx',cell_error_samplesValue_Title,'SortedErrors','B1');
    xlswrite('Error\Sorted_error_test_samplesValue.xlsx',cell_error_test_samplesValue,'SortedErrors','B2');
    xlswrite('Error\Sorted_error_test_samplesValue.xlsx',testMeanError,'SortedErrors','D2');
end

[error_train_samplesValue, error_train_samplesIndex] = sort(abs(A_error_train_samples),'descend');
cell_error_train_samplesValue = [train_speciesName(error_train_samplesIndex) num2cell(A_error_train_samples(error_train_samplesIndex))];
if saveFlag == 1
    xlswrite('Error\Sorted_error_train_samplesValue.xlsx',cell_error_samplesValue_Title,'SortedErrors','B1');
    xlswrite('Error\Sorted_error_train_samplesValue.xlsx',cell_error_train_samplesValue,'SortedErrors','B2');
    xlswrite('Error\Sorted_error_train_samplesValue.xlsx',trainMeanError,'SortedErrors','D2');
    dlmwrite('Error\A_error_test_samples.txt',A_error_test_samples,'precision',6);
    dlmwrite('Error\A_error_train_samples.txt',A_error_train_samples,'precision',6);
end

% figure of training prediction vs reference data
if(~isdir('Figure'))
    mkdir('Figure');
end
figure
plot(train_Y, predicted_train_Y, '.'); hold
plot(train_Y(find(abs(A_error_train_samples)>=1)), predicted_train_Y(find(abs(A_error_train_samples)>=1)), 'g.'); hold on
plot(train_Y(find(abs(A_error_train_samples)>=2)), predicted_train_Y(find(abs(A_error_train_samples)>=2)), 'r.'); hold on
title(['Train samples, R^2 : ' num2str(R_square_train_samples)]);
xlabel('Original value');
ylabel('ANN prediction');
xPosition_min = min(train_Y);
xPosition_max = max(train_Y);
yPosition_min = min(predicted_train_Y);
yPosition_max = max(predicted_train_Y);
text(xPosition_min+(xPosition_max-xPosition_min)*0.1,yPosition_min+(yPosition_max-yPosition_min)*0.9,[num2str(Ratio_less_1_train_samples) '% less than 1 kcal'],'fontsize',14)
text(xPosition_min+(xPosition_max-xPosition_min)*0.1,yPosition_min+(yPosition_max-yPosition_min)*0.82,[num2str(Ratio_less_2_train_samples) '% less than 2 kcal'],'fontsize',14)
set(gca,'fontsize',16);
set(gcf, 'PaperPositionMode', 'manual');
set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperPosition', [2 1 8 6]);
filename2 = ['Figure\trainSamples.tiff'];
if saveFlag == 1
	print('-dtiff','-r1000', filename2); 
end

% figure of test prediction vs reference data 
figure
plot(test_Y, predicted_test_Y, '.'); hold on
plot(test_Y(find(abs(A_error_test_samples)>=1)), predicted_test_Y(find(abs(A_error_test_samples)>=1)), 'g.'); hold on
plot(test_Y(find(abs(A_error_test_samples)>=2)), predicted_test_Y(find(abs(A_error_test_samples)>=2)), 'r.'); hold on
title(['Test samples, R^2 : ' num2str(R_square_test_samples)]);
xlabel('Original value');
ylabel('ANN prediction');
xPosition_min = min(test_Y);
xPosition_max = max(test_Y);
yPosition_min = min(predicted_test_Y);
yPosition_max = max(predicted_test_Y);
text(xPosition_min+(xPosition_max-xPosition_min)*0.1,yPosition_min+(yPosition_max-yPosition_min)*0.9,[num2str(Ratio_less_1_test_samples,3) '% less than 1 kcal'],'fontsize',14);
text(xPosition_min+(xPosition_max-xPosition_min)*0.1,yPosition_min+(yPosition_max-yPosition_min)*0.82,[num2str(Ratio_less_2_test_samples,3) '% less than 2 kcal'],'fontsize',14);
set(gca,'fontsize',16);
set(gcf, 'PaperPositionMode', 'manual');
set(gcf, 'PaperUnits', 'inches');
set(gcf, 'PaperPosition', [2 1 8 6]);

filename1 = ['Figure\testSamples.tiff'];
if saveFlag == 1
    print('-dtiff','-r1000', filename1 );
end

close(findall(0,'tag','Msgbox_ '))










