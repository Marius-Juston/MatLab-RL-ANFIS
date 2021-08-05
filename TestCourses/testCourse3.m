
% Generation of Test Course 3

% Input: L ----- Horizontal length of TC3
%        R ----- Turn radius
%        n ----- Number of "dips"
%        cStep - Curve stepsize

function testCourse3(L, R, n, cStep)

% number of quarter turns
numQ = 2 + 4 * (n - 1);

if (L <= R * numQ)
    error('LENGTH TOO SHORT TO ACCOMODATE DIPS; INCREASE L, DECREASE R, OR DECREASE n')
end

% compute x-coordinate of first corner-point
x1 = (L / 2) - R * (numQ / 2) + R;

% initialize corner-point data with first 2 corner-points
cpData = [x1,   0,      R;
          x1,   -2 * R, R];
      
% initialize current corner-point coordinates
x = x1;
y = -2 * R;

% if there is more than one dip
if (n > 1)
    % for the remainder of the dips
    for i = 2:n
        % add dip corner-points to the corner-point data array
        cpData = [cpData;
                  x+2*R,    y,      R;
                  x+2*R,    y+2*R,  R;
                  x+4*R,    y+2*R,  R;
                  x+4*R,    y,      R];
        % update current corner-point x-coord (y-coord stays the same)
        x = x + 4 * R;
    end
end

% add the final corner-point to the corner-point data array
cpData = [cpData;
          L,    -2*R,   R];

% generate waypoints from corner-point data
generateWaypoints(cpData, cStep);
