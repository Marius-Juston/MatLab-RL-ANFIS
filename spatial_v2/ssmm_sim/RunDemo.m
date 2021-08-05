%% Skid-Steer Mobile Manipulator Model and Simulation Demonstration
% RunDemo: Runs a quick demonstration in just one command of the 
%          of the Skid-Steer Mobile Manipulator, i.e. this file
%          does all the configuration, model construction, simulation 
%          and display of the results.
%
%          For a step by step execution and explanation of the model
%          construction and simulation, please see the REAME.txt file
%          in this folder.
%
%%         WARNING: 
%                   The complete simulation takes about 15 minutes
%                   in a PC with an Intel(R) Core(TM) i7/3740QM CPU
%                   running a at 2.7 GHz on Windows 7 64 bits, \
%                   and 64 Gb RAM.
%                   
%                   To test the Demo for a shorter period of time,
%                   change the value of the stop time for the 'sim'
%                   command in line 54.
%
% Copyright (c) 2015.12.20 
%   Sergio Aguilera-Marinovic (sfaguile@uc.cl)
%   Miguel Torres-Torriti     (mtorrest@ing.puc.cl)
%   Robotics and Automation Laboratory
%   Pontificia Universidad Catolica de Chile
%   http://ral.ing.puc.cl/ssmm.htm
% 
% Version 2.0 - 2015.12.20

clear all
close all
clc
help RunDemo
disp('Press any key to continue...')
pause

% Set up the search path for the Spatial Toolbox to become available.
% These only works with the modified startup.m supplied with this files.
% You may comment out these lines if the path for the Spatial Toolbox 
% is already parth of Matlab's search path, or replace the startup.m file
% in your Spatial Toolbox with the one included in this distribution.
disp('Setting the search path for the Spatial Toolbox to become available...')
cd ..
startup;
cd ssmm_sim

% Load the model definition.
disp('Loading the model definition...')
SSMM_model_Torque_3DOF;

% Run the simulation.
disp('Running the simulation...')
disp('Warning: This might take about 15 minutes using the default stop time.')
SimOut = sim('SSMM_sim_Torque_3DOF','StopTime', '21.0', 'ReturnWorkspaceOutputs', 'on');
Arm_Angles = SimOut.get('Arm_Angles');
Fout = SimOut.get('Fout');
Fout1 = SimOut.get('Fout1');
PosVel = SimOut.get('PosVel');
Reference_Pos = SimOut.get('Reference_Pos');
tout = SimOut.get('tout');
xout = SimOut.get('xout');

% Plot the results.
PlotResults;