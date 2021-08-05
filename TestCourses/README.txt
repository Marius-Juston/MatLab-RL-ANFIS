
The testCourse1-4 functions take test course parameters as input and create an nx2 array of [x, y] pairs describing coordinates of waypoints. The array is written to the
workspace as 'waypoints'.

Execute testCourse functions (with valid parameters) from the command window and then execute the plotTestCourse function to view the path that has been created.
Examples that demonstrate use can be found in the examples.m file.
Additional documentation describing input parameters for each of the functions are found at the top of the testCourse function files.

The testCourse1 function is hardcoded to produce waypoints. The testCourse2-4 functions utilize the generalized test course generator to convert the test course input
parameters into corner-point data, and then use the corner-point data to generate waypoints. Custom test courses can also be created by manually specifying corner-point
data and calling the generateWaypoints function. The test course generator can create any test course that consists of straight segments and circular curvatures (e.g. Test
Courses 1-4 can be created using the generator, but Test Course 5 can't because the curvatures are non-circular). An example of generating a custom test course can be found
in the customTestCourse.m file.