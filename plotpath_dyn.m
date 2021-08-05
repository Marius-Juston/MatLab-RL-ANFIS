% this function can be used after simulations to compare robot path with
% desired path
function plotpath_dyn()

% import variables from workspace
waypoints = evalin('base', 'path');
xout = evalin('base', 'xout');

% extract x and y values from path describing positions of waypoints
x_wp = waypoints(:,1);
y_wp = waypoints(:,2);
% extract x and y values from xout describing robot motion
x_robot = xout(5,:);
y_robot = xout(6,:);

% plot waypoints
plot(x_wp, y_wp, '*r'); hold on
% insert starting point to the beginning of waypoint coordinate vectors
% (only valid if starting point is the origin!)
x_wp = [0; x_wp];
y_wp = [0; y_wp];
% plot waypoint trajectories
plot(x_wp, y_wp, ':r'); hold on
% plot robot path of motion
plot(x_robot, y_robot)

end 
