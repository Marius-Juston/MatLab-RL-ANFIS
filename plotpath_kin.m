% this function can be used after simulations to compare robot path with
% desired path
function plotpath_kin()

% import variables from workspace
waypoints = evalin('base', 'path');
out = evalin('base', 'out');
xout = out.xout;

% extract x and y values from path describing positions of waypoints
x_wp = waypoints(:, 1);
y_wp = waypoints(:, 2);
% extract x and y values from xout describing robot motion
x_robot = xout(:, 2);
y_robot = xout(:, 3);

% plot waypoint trajectories
plot(x_wp, y_wp, ':*r'); hold on
% plot robot path of motion
plot(x_robot, y_robot)

end