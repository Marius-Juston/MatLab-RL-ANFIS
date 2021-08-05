
% This function takes corner point data containing coordinates and radius
% of curvature and generates a path of waypoints.

% Input: cornerPointData - Data containing x and y coordinates and curve
%                          radius of corner-points. At least 2
%                          corner-points must be provided.
%        cStep ----------- Curve step-size. (This auto-adjusts for 
%                          symmetry, final curve step-size will be equal to
%                          or slightly smaller than what is input)

function generateWaypoints(cornerPointData, cStep)

% initialize waypoints array
waypoints = [];

% number of corner-points
[num, ~] = size(cornerPointData);

% initialize current corner-point as the origin
cp_curr.x = 0;
cp_curr.y = 0;
cp_curr.radius = 0;
% initialize next corner-point from corner-point data
cp_next.x = cornerPointData(1, 1);
cp_next.y = cornerPointData(1, 2);
cp_next.radius = cornerPointData(1, 3);
% initialize next theta_{global}
tG_next = thetaGlobal(cp_curr, cp_next);
% initialize current cut length
L_cut_curr = 0;

% for all corner-points except the last one
for i = 1:(num - 1)
    % set previous corner-point
    cp_prev = cp_curr;
    % set current corner-point
    cp_curr = cp_next;
    % set next corner-point
    cp_next.x = cornerPointData((i + 1), 1);
    cp_next.y = cornerPointData((i + 1), 2);
    cp_next.radius = cornerPointData((i + 1), 3);
    
    % set current theta_{global}
    tG_curr = tG_next;
    % compute next theta_{global}
    tG_next = thetaGlobal(cp_curr, cp_next);
    % compute theta_{relative}
    tR = tG_next - tG_curr;
    tR = abs_lt_pi(tR);
    % if left curve
    if (tR > 0)
        % set curve flag
        curve = 'left-';
    % else if right curve
    elseif (tR < 0)
        % set curve flag
        curve = 'right';
    % else if no curve, straight
    elseif (tR == 0)
        % set curve flag
        curve = 'str8t';
    end
    % if no curve, back
    if (tR == pi)
        % set curve flag
        curve = 'back-';
    end
    
    % if no curvature, straight
    if (curve == 'str8t')
        % set current corner-point to previous corner-point, so it's as
        % if the current corner-point was never even there
        cp_curr = cp_prev;
    % else if no curvature, back
    elseif (curve == 'back-')
        % append current corner-point to waypoints array
        waypoints = [waypoints; cp_curr.x, cp_curr.y];
        % reset current cut length, this behaves similarly to
        % initialization
        L_cut_curr = 0;
    % else there is curvature
    else
        % if current corner-point radius is 0
        if (cp_curr.radius == 0)
            % append current corner-point to waypoints array
            waypoints = [waypoints; cp_curr.x, cp_curr.y];
        % else waypoints describing the curvature are computed
        else
            % compute phi 1 and 2
            phi_1 = (pi - abs(tR)) / 2;
            phi_2 = (pi / 2) - phi_1;

            % compute length of hypotenuse
            H = cp_curr.radius / sin(phi_1);

            % compute c-step angle, adjust for symmetry
            phi_s = cStep / cp_curr.radius;
            num_cSteps = ceil(2 * phi_1 / phi_s);
            phi_s = 2 * phi_1 / num_cSteps;

            % compute length from previous corner-point to current corner-point
            L = pythag(cp_prev, cp_curr);
            % set previous cut length
            L_cut_prev = L_cut_curr;
            % compute current cut length
            L_cut_curr = cp_curr.radius * tan(phi_2);
            % sum of cut lengths
            cuts = L_cut_prev + L_cut_curr;
            % length and sum of cut lengths must now be rounded before
            % comparison to prevent numerical errors that will result in 2
            % waypoints being placed really close to one another, this is
            % especially important for edge cases where cuts == L (flush
            % curvatures), such as those found in Test Courses 3 and 4
            L = round(L, 4);
            cuts = round(cuts, 4);
            % if there are conflicting curvatures
            if (cuts > L)
                error(['CONFLICTING CURVATURES - CORNER POINT ', num2str(i)])
            % else if there is some length of straight between curvatures
            elseif (cuts < L)
                % compute coordinates of straight-endpoint
                x_newWP = cp_prev.x + (L - L_cut_curr) * cos(tG_curr);
                y_newWP = cp_prev.y + (L - L_cut_curr) * sin(tG_curr);
                % append to waypoints array
                waypoints = [waypoints; x_newWP, y_newWP];
            % else the curvatures are flush and no straight-endpoint is placed
            end

            if (curve == 'right')
                % compute phi_{Hypothenuse}
                phi_H = tG_next - phi_1;
                phi_H = abs_lt_pi(phi_H);
                % initialize phi_{point-placement}
                phi_pp = tG_curr + (pi / 2);
                phi_pp = abs_lt_pi(phi_pp);
                % compute phi_{end}
                phi_end = phi_pp - 2 * phi_2;
                % compute coordinates of center of curvature
                x_cc = cp_curr.x + H * cos(phi_H);
                y_cc = cp_curr.y + H * sin(phi_H);

                % while there are still curvature waypoints to add
                % phi_pp and phi_end are rounded to prevent numerical
                % errors
                while (round(phi_pp, 4) > round(phi_end, 4))
                    % decrement phi_{point-placement}
                    phi_pp = phi_pp - phi_s;
                    % compute coordinates of new waypoint
                    x_newWP = x_cc + cp_curr.radius * cos(phi_pp);
                    y_newWP = y_cc + cp_curr.radius * sin(phi_pp);
                    % append to waypoints array
                    waypoints = [waypoints; x_newWP, y_newWP];
                end

            elseif (curve == 'left-')
                % compute phi_{Hypothenuse}
                phi_H = tG_next + phi_1;
                phi_H = abs_lt_pi(phi_H);
                % initialize phi_{point-placement}
                phi_pp = tG_curr - (pi / 2);
                phi_pp = abs_lt_pi(phi_pp);
                % compute phi_{end}
                phi_end = phi_pp + 2 * phi_2;
                % compute coordinates of center of curvature
                x_cc = cp_curr.x + H * cos(phi_H);
                y_cc = cp_curr.y + H * sin(phi_H);
                
                % while there are still curvature waypoints to add
                % phi_pp and phi_end are rounded to prevent numerical
                % errors
                while (round(phi_pp, 4) < round(phi_end, 4))
                    % increment phi_{point-placement}
                    phi_pp = phi_pp + phi_s;
                    % compute coordinates of new waypoint
                    x_newWP = x_cc + cp_curr.radius * cos(phi_pp);
                    y_newWP = y_cc + cp_curr.radius * sin(phi_pp);
                    % append to waypoints array
                    waypoints = [waypoints; x_newWP, y_newWP];
                end

            end
            
        end
        
    end
    
end

% set previous corner-point
cp_prev = cp_curr;
% set current corner-point
cp_curr = cp_next;
% compute length from previous corner-point to current corner-point
L = pythag(cp_prev, cp_curr);
% set previous cut length
L_cut_prev = L_cut_curr;

% if there is conflicting curvature at the end
if (L < L_cut_prev)
    error(['CONFLICTING CURVATURE - CORNER-POINT ', num2str(num - 1)])
% else if the last corner-point ends in a straight
elseif (L > L_cut_prev)
    % append current corner-point to waypoints array
    waypoints = [waypoints; cp_curr.x, cp_curr.y];
end

% write waypoints array to workspace
assignin('base', 'path', waypoints);

end


%=========================== HELPER FUNCTIONS =============================

% pythagorean theorem
function h = pythag(cp1, cp2)

h = sqrt((cp1.x - cp2.x)^2 + (cp1.y - cp2.y)^2);

end

% computes the angle of corner-point 2 wrt corner-point 1 relative to
% global coordinates
function tG = thetaGlobal(cp1, cp2)

tG = atan2(cp2.y - cp1.y, cp2.x - cp1.x);
% set return angle to be between -pi and pi
tG = abs_lt_pi(tG);

end

% "abs(angle) less than pi" - sets angle so that -pi < angle <= pi
function ret = abs_lt_pi(angle)

while (angle > pi)
    angle = angle - 2 * pi;
end
while (angle <= -pi)
    angle = angle + 2 * pi;
end

ret = angle;

end