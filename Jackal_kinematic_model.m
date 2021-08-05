%this is the model file for a kinematic differential steer model of the
%Jackal UGV. The first section must be re-run (because pathcount must be reset) every
%time you run a simulation in simulink. The second section displays a graph
%of the robot path traveled overlayed on the ideal path

close all; clear all; clc;

% ========================== Path Generator ==========================
%Below is the path that we are trying to have the model follow in the
%simulation. It is comprised of a list of target positions of the form 
%[x1 y1;x2 y2; ...;xn yn]

% path=[3 0;
%       0 1;
%       5 3;
%       5 -2;
%       5 2];
path = [5,   0;
             5,  -5;
             10, -5;
             10, 5;
             15, 5;
             15, 0;
             20, 0];
%testCourse3(16, 1.22, 3, 1.2);
%testCourse3(18, 1.4, 3, 1.2);
%testCourse2(15, 5, 6, 6, 6, 2/pi, 1, 0.8)
%testCourse2(18, 5, 6, 6, 6, 1.22, 1, 0.8);
path=[0 0;path];
%flip
path(:,2) = -1*path(:,2);
[pathlength,~]=size(path);% used by path error calculator

speed=2; %maximum wheel speed in m/s
width=.323; %width between the left and right wheels

init=[0,0,0]; % initial theta,x,y