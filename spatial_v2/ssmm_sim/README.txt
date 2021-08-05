% Skid-Steer Mobile Manipulator Model and Simulation Using the
% Spatial Toolbox for Rigid Body Dynamics
% 
% Copyright (c) 2015.12.20 
%   Sergio Aguilera-Marinovic (sfaguile@uc.cl)
%   Miguel Torres-Torriti     (mtorrest@ing.puc.cl)
%   Robotics and Automation Laboratory
%   Pontificia Universidad Catolica de Chile
%   http://ral.ing.puc.cl/ssmm.htm
% 
% Version 2.0 - 2015.12.20
%
% Description
%  These Matlab scripts show how to build the model for an SSMM and 
%  simulate it using the Spatial Toolbox for rigid body dynamics modeling
%  developed by Roy Featherstone available at http://royfeatherstone.org.
%
%  The model considers a floating base with four wheels and a 3-DOF arm.
%  It is possible to easily add more degrees of freedom to the
%  arm by copying the data structure for the 3-DOF arm and updating the
%  parent link data where appropriate.  
%
%
% Instructions
%
%  1. Prerequisites in addition to a standard installation of Matlab and 
%     Simulink is two download and setup the Spatial Toolbox version 2 by 
%     Roy Featherstone available at http://royfeatherstone.org.
%
%  2. Initialize the Spatial Toolbox with the command 'startup.m', which
%     adds its installation path to Matlab's environment list of paths.
%
%  3. Change the directory to the location of the SSMM script files 
%     (this model and simulation files).
% 
%  4. Run the SSMM_model_Torque_3DOF.m file, it will create and store the SSMM model
%     in variable 'model'. At the end of these code, few examples are
%     presented
%
%  6. Run the Simulink simulation file SSMM_sim_Torque_3DOF.slx.  The output of the 
%     simulation is stored in the variable xout, which is a 27x1xN
%     array structure.  To reduce the singleton dimension you may execute
%     res = squeeze(xout), which will store the results in variable res
%     23xN array.  
% 
%     The 23 model state variables are the following:
%     1. The floating base varaibles:
%
%       x = [x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13]';
%            |_________| |______| |_______| |_________|
%                 |          |        |          |->Linear Velocity in
%                 |          |        |               F1 Coordinates
%                 |          |        |
%                 |          |        |->Angular Velocity in
%                 |          |             F1 Coordinates
%                 |          |        
%                 |          |->Position relative to F_0
%                 |
%                 |->Orientation Quaternion
%
%     2. The 1-DOF joint positions:
%
%       q = [q1 q2 q3 q4 q5 q6 q7]'
%             |________| |______|
%                 |         |
%                 |         |->Arm joint positions
%                 |->Wheel joint positions
%
%     3. The 1-DOF joint velocities:
%
%       qd = [qd1 qd2 qd3 qd4 qd5 qd6 qd7]'
%             |_____________| |_________|
%                    |              |
%                    |              |->Arm joint velocities
%                    |->Wheel joint velocities
%
%     The full state vector with results of the simulation is stored in
%     the variable xout and contains the previous vectors, as follows:
%
%       xout = [x q qd]'
%
%  7. At the end of the simulation you may execute:
%     res = squeeze(xout)
%     plot(tout,res(11,:)) % plots the longitudinal velocity of the mobile
%                          % base
%     plot(tout,res(5,:))  % plots the longitudinal displacement of the
%                          % mobile base
%     plot(tout,res(25:27,:)) % plots the arm positions
% 
%     The following command renders a 3D representation of the 
%     model and its motion using showmotion provided with the Spatial
%     Toolbox:
%    
%     showmotion(model,tout,[fbanim(xout);squeeze(xout(14:20,:,:))])
%
%  8. To draw the trajectory of the end-effector, run:
%
%     Draw_End_Effector
%
%     Then close the showmotion window if the previous step was executed
%     and re-run the previous showmotion step:
%
%     showmotion(model,tout,[fbanim(xout);squeeze(xout(14:20,:,:))])
%
%     Alternatively, you may run:
%     
%     PlotResults
%
% 