
% Generation of Test Course 4

% Input: R1 ---- Turn radius 1
%        R2 ---- Turn radius 2
%        n ----- Number of laps
%        cStep - Curve stepsize

function testCourse4(R1, R2, n, cStep)

% corner-point data describing a full lap around TC4
cpLap = [0,     R1,     R1;
         2*R1,  R1,     R1;
         2*R1,  -R1,    R1;
         0,     -R1,    R1;
         0,     R2,     R2;
         -2*R2, R2,     R2;
         -2*R2, -R2,    R2;
         0,     -R2,    R2
         0,     0,      R2];
     
% initialize corner-point data array
cpData = [];
% for n number of laps
for i = 1:n
    % append lap to corner-point data array
    cpData = [cpData; cpLap];
end

% generate waypoints from corner-point data
generateWaypoints(cpData, cStep);