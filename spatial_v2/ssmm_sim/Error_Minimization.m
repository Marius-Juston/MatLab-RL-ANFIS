function q_min = Error_Minimization(model, xfb, q,q_ant)

persistent PROD_X
persistent Q_ANT

if isempty(PROD_X)
   PROD_X = 1;
end

if isempty(Q_ANT)
   Q_ANT = [0 0 0];
end


qn = xfb(1:4);                            % unit quaternion fixed-->f.b.
r = xfb(5:7);                             % position of f.b. origin
Xa{6} = plux( rq(qn), r );            	  % xform fixed --> f.b. coords

referencia = [r(1)-1.2; 1.7; 3];

q_ini = q(5:7);

maxIter = 20;
%options = optimoptions(@lsqnonlin, 'MaxIter', maxIter, 'Display', 'off');
options = optimset('MaxIter', maxIter, 'Display', 'off');

if(PROD_X == 1)
    q_min = lsqnonlin(@(x) End_Effector_Position_Error(x,model,qn, r, referencia), q_ini, [-pi -pi -pi], [pi pi pi], options);
    Q_ANT = q_min;
else
    q_min = Q_ANT;
end

if(PROD_X == maxIter*10)
   PROD_X = 0; 
end
PROD_X = PROD_X +1;
end


