
% Generation of Test Course 2

% Input: L1-2, H1-3, R - Parameters describing the geometry of TC2 (see diagram for details)
%        n ------------- Number of laps
%        cStep --------- Curve stepsize

function testCourse2(L1, L2, H1, H2, H3, R, n, cStep)

% corner-point data describing a full lap around TC2
cpLap = [L1,    0,          R;
         L1,    -H1,        R;
         0,     -H1,        R;
         0,     -H1-H2,     R;
         L1,    -H1-H2,     R;
         L1,    -H1-H2-H3,  R;
         -L2,   -H1-H2-H3,  R;
         -L2,   0,          R;
         0,     0,          R];

% initialize corner-point data array
cpData = [];
% for n number of laps
for i = 1:n
    % append lap to corner-point data array
    cpData = [cpData; cpLap];
end

% generate waypoints from corner-point data
generateWaypoints(cpData, cStep);