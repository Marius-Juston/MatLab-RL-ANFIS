
% plots the test course after a test course function has been generated
% using one of the test course functions

function plotTestCourse()

% read in waypoints array from workspace
waypoints = evalin('base', 'waypoints');

% extract x and y values from waypoints array
x = waypoints(:, 1);
y = waypoints(:, 2);

% plot waypoints
plot(x, y, 'r*'); hold on

% append 0 to the beginning of the x and y vectors (the origin)
% this is because the origin technically isn't a waypoint, but is included
% to visualize the full path, which starts at the origin; this is only for
% cosmetic purposes
x = [0; x];
y = [0; y];
% plot path
plot(x, y, 'r--'); hold on

% plot a black marker at the origin to represent starting point of vehicle
plot(0, 0, 'ks', 'MarkerFaceColor', 'k')

% THE REST OF THE CODE IS FOR SCALING PURPOSES
% get x and y min and max values
x_min = min(x);
x_max = max(x);
y_min = min(y);
y_max = max(y);
% find the larger range between the sets of x and y values
range = max(x_max - x_min, y_max - y_min);
% compute limits for axes
x_ub = x_max + 0.1 * range;
x_lb = x_ub - 1.2 * range;
y_ub = y_max + 0.1 * range;
y_lb = y_ub - 1.2 * range;
% change axis limits
axis([x_lb, x_ub, y_lb, y_ub])

set(gcf, 'Position', [600, 150, 800, 800])
