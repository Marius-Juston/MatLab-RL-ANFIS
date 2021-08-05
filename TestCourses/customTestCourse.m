
% STEP 1: SPECIFY CORNER-POINT DATA
% Corner-point data is an nx3 array of [x, y, R] triples. x and y are the
% coordinates of the corner-point and R is the radius of curvature. At
% least 2 triples must be specified. Conflicting curvatures will result in
% an error during generation. The radius specified for the last
% corner-point has no effect on waypoint creation, but a value must still
% be given to make the generator happy.

cpData = [4,    12,     5;
          4,    20,     5;
          18,   20,     3;
          18,   13,     0.5;
          10,   13,     0.5;
          10,   12,     0.5;
          18,   12,     0.5;
          18,   9,      3;
          8,    4,      1;
          10,   2,      1;
          12,   4,      1;
          6,    8,      5;
          6,    12,     0.5;
          7,    12,     0.5;
          7,    13,     0.5;
          6,    13,     0.5;
          6,    14,     0.5;
          7,    14,     0.5;
          7,    15,     0.5;
          6,    15,     0.5;
          6,    16,     0.5;
          7,    16,     0.5;
          7,    17,     0.5;
          16,   17,     1;
          16,   15,     1;
          14,   15,     1;
          14,   17,     1;
          16,   17,     1];
      
% STEP 2: GENERATE WAYPOINTS
% Execute the generateWaypoints function. Inputs to the function are the
% corner-point data array previously created and the desired curvature
% step size.

generateWaypoints(cpData, 0.5);

% STEP 3: VIEW TEST COURSE (OPTIONAL)
% The plotTestCourse function can be used to view the generated path of
% waypoints. The black square indicates starting point, red asterisks
% indicate waypoints, red dashed lines indicates path.

%plotTestCourse