%% use containers.map for fuzzy membership function values
clear all
addpath('func')
%----------------- distance
v_distKeySet = {'far_left','close_left','zero','close_right','far_right'};
v_distValueSet = { [  -10,1;  -5,1;   -4,0;   10,0], ...
                 [  -10,0;  -5,0;   -4,1;   -1.5,1; -1,0;   10,0 ], ...
                 [  -10,0;  -1.5,0; -1,1;   1,1;    1.5,0;  10,0 ], ...
                 [  -10,0;  1,0;    1.5,1;  4,1;    5,0;    10,0 ], ...
                 [  -10,0;  4,0;    5,1;    10,1] ...
                };
% distance membership function values, sets of value of either 4 or 6.
v_distMFV = containers.Map( v_distKeySet, v_distValueSet); 

%------------------ front angle
v_frontAngleKeySet = {'far_left','near_left','close_left',...
                    'zero', ...
                    'close_right','near_right','far_right'};
v_frontAngleValueSet = {  [  -0.45,-0.2925,-0.27,0.45;1,1,0,0]',... far left,
                        [  -0.45,-0.2925,-0.27,-0.16874,-0.14624,0.45;0,0,1,1,0,0 ]', ... near left
                        [  -0.45,-0.16874,-0.14624,-0.045,-0.0225,0.45;0,0,1,1,0,0 ]', ... close left
                        [  -0.45,-0.045,-0.0225,0.0225,0.045,0.45; 0,0,1,1,0,0]', ... zero     
                        [  -0.45,0.0225,0.045,0.14624,0.16874,0.45; 0,0,1,1,0,0 ]', ... close right
                        [  -0.45,0.14624,0.16874,0.27,0.2925,0.45; 0,0,1,1,0,0]', ... near right
                        [  -0.45,0.27,0.2925,0.45;0,0,1,1]' ... far right
                      };
% frontAngle membership function values, sets of value of either 4 or 6.
v_frontAngleMFV = containers.Map( v_frontAngleKeySet, v_frontAngleValueSet );

%------------------- orientation
v_orientationKeySet = {'far_left','close_left','zero','close_right','far_right'};
v_orientationValueSet = { [   -0.7854,-0.4363,-0.25,0.7854;1,1,0,0]', ... far_ left
                        [   -0.7854,-0.4363,-0.25,-0.1,-0.0524,0.7854;0,0,1,1,0,0]', ... close_left
                        [   -0.7854,-0.1,-0.0333,0.0333,0.1,0.7854;0,0,1,1,0,0]', ... zero
                        [   -0.7854,0.0524,0.1,0.25,0.4363,0.7854;0,0,1,1,0,0]', ... close right
                        [   -0.7854,0.25,0.4363,0.7854;0,0,1,1]' ... far right
                       };
% orientation membership function values, sets of value of either 4 or 6.
v_orientationMFV= containers.Map( v_orientationKeySet, v_orientationValueSet );

%------------------- thetaClose
v_thetaCloseKeySet = {'far_left','near_left','close_left',...
                    'zero', ...
                    'close_right','near_right','far_right'};
v_thetaCloseValueSet = {  [  -0.45,-0.2925,-0.27,0.45;1,1,0,0]',... far left,
                        [  -0.45,-0.2925,-0.27,-0.16874,-0.14624,0.45;0,0,1,1,0,0 ]', ... near left
                        [  -0.45,-0.16874,-0.14624,-0.045,-0.0225,0.45;0,0,1,1,0,0 ]', ... close left
                        [  -0.45,-0.045,-0.0225,0.0225,0.045,0.45; 0,0,1,1,0,0]', ... zero     
                        [  -0.45,0.0225,0.045,0.14624,0.16874,0.45; 0,0,1,1,0,0 ]', ... close right
                        [  -0.45,0.14624,0.16874,0.27,0.2925,0.45; 0,0,1,1,0,0]', ... near right
                        [  -0.45,0.27,0.2925,0.45;0,0,1,1]' ... far right
                      };
v_thetaCloseMFV = containers.Map( v_thetaCloseKeySet, v_thetaCloseValueSet);

%------------------- thetaNear
v_thetaNearKeySet = {'far_left','close_left','zero','close_right','far_right'};
v_thetaNearValueSet = { [   -0.45,-0.2925,-0.2475,0.45;1,1,0,0]',... far left
                        [   -0.45,-0.2925,-0.2475,-0.135,-0.09,0.45;0,0,1,1,0,0]',...close left
                        [   -0.45,-0.135,-0.09,0.09,0.135,0.45;0,0,1,1,0,0]',...zero
                        [   -0.45,0.09,0.135,0.2475,0.2925,0.45;0,0,1,1,0,0]',...close right
                        [   -0.45,0.2475,0.2925,0.45;0,0,1,1]',...far right
                       };
v_thetaCloseMFV = containers.Map( v_thetaNearKeySet, v_thetaNearValueSet );

                                                     