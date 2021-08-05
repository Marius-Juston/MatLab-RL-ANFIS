
% input:  L ----- Length of straights
%         R ----- Radius of curvature
%         theta - Angle between straights (in degrees)
%         cStep - Curve stepsize
% output: waypoints describing Test Course 1 (doesn't include origin)

function testCourse1(L, R, theta, cStep)

% convert theta from degrees to radians
theta = theta * pi / 180;

% compute (big) phi1
phi1 = (pi - theta) / 2;
% compute L1 and L2
L2 = R / tan(phi1);
L1 = L - L2;

% compute (big) phi2
phi2 = (pi / 2) - phi1;

% compute (little) phi, this is the c-step angle
cStepAng = cStep / R;

% center of curvature
C = [L1, -R];

% initialize Test Course 1 waypoints array with first waypoint
waypoints = [L1, 0];

% initialize stepper angle
stprAng = cStepAng;
% while there are still more curvature waypoints to append
while (stprAng < 2 * phi2)
    % compute next waypoint
    nextWP = [C(1) + R * sin(stprAng), C(2) + R * cos(stprAng)];
    % append next waypoint to waypoints array
    waypoints = [waypoints; nextWP];
    % increment stepper angle
    stprAng = stprAng + cStepAng;
end
 
% compute waypoint that begins the 2nd straight, append to waypoints array
nextWP = [L + L2 * sin(theta), -L2 * cos(theta)];
waypoints = [waypoints; nextWP];
% compute waypoint that ends the 2nd straight, append to waypoints array
nextWP = [L1 + L * sin(theta), -L * cos(theta)];
waypoints = [waypoints; nextWP];

% write waypoints array to workspace
assignin('base', 'waypoints', waypoints);