function  [f2, ud2, fcone2] = gcontact2( K, D, mu, p, pd, u )

% gcontact  calculate 2D/3D ground reaction forces due to compliant contact
% [f,ud,fcone] = gcontact(K,D,mu,p,pd,u)  calculates the ground-reaction
% forces acting on a set of points due to contact with a compliant ground
% plane.  In 3D, the x-y plane is the ground plane, and z is up.  In 2D,
% the x axis is the ground plane and y is up.  K, D and mu are scalars
% giving the stiffness, damping and friction coefficients of the ground
% plane.  p and pd are (nD)x(np) matrices giving the positions and
% velocities of a set of np points in nD-dimensional space (nD=2 or 3).
% gcontact uses the size of p to determine whether it is working in 2D or
% 3D space.  u is an (nD-1)x(np) matrix containing the tangential
% deformation state variables used to implement the friction model.  f is
% an (nD)x(np) matrix of calculated ground-reaction forces.  If f(nD,i)==0
% then point i is not in contact; and if f(nD,i)>0 then point i is in
% contact.  ud is the time derivative of u; and fcone is a 1x(np) matrix
% indicating the stick/slip status of each point.  If fcone(i)<=1 then
% point i is sticking.  This can happen only if point i is in contact.  To
% facilitate use with Simulink, if gcontact is called with only a single
% return value then it returns the concatenation of f, ud and fcone (i.e.,
% the return value is [f;ud;fcone]).  To model a frictionless surface,
% gcontact can be called as follows: f=gcontact(K,D,0,p,pd), where p, pd
% and f are all 1x(np) matrices containing only the normal components of
% position, velocity and reaction force.

% Implementation note:  This function implements the nonlinear
% spring-damper model described in Azad & Featherstone "Modelling the
% Contact Between a Rolling Sphere and a Compliant Ground Plane", ACRA
% 2010, Brisbane, Australia, Dec. 1-3.  However, the implementation here is
% for points rather than spheres.

% Normal force calculation

A = 0;
sigma = 0.5;
x0 = 6;
y0 = 0;

alt = A*exp(-(((p(1,:)-x0).^2)/(2*sigma^2)+((p(2,:)-y0).^2)/(2*sigma^2)));


z = p(end,:)-alt;
zd = pd(end,:);
zr = sqrt(max(0,-z));

n = [0;0;1];
d = 0;
vec = diag(sqrt(sum(pd'.^2,2)))\pd';

aux = n'*vec';
%p_perp = n*((d-n'*p)./(n'*n))+p;
% p_perp = p-n*(n'*p);
%p_r = (bsxfun(@times,vec,((d-n'*p)./(n'*vec'))'))'+p;
% p_r = (bsxfun(@times,vec,((n'*p)./(n'*vec'))'))'+p;
% p_ep = p_perp-p_r;
% vec_ep = diag(sqrt(sum(p_ep'.^2,2)))\p_ep';

% u = p_ep(1:end-1,:);



fn = zr .* ((-K)*z - D*zd);

if mu == 0			% special case: modelling frictionless
  f = max( 0, fn );		% contact, so return the normal force now
  f2 = max(0,fn);
  return
end

% Algorithm for full normal+tangent force calculation: (1) set all output
% variables to their correct no-contact values; (2) correct all the values
% that are wrong because their respective points are in contact.  Step (2)
% is subdivided into (2a) calculate correct values for sticking; (2b)
% adjust the values for those points that are found to be slipping; (2c)
% make the corrections to the output variables.

% Step 1: set output variables to correct no-contact values

[nd,np] = size(p);
f = zeros(nd,np);
f2 = zeros(nd,np);

ud = (-K/D) * u;
ud2 = (-K/D) * u;
fcone = repmat(2,1,np);			% 2 is just an arbitrary value > 1
fcone2 = repmat(2,1,np);


in_ctact = fn > 0 & sqrt(aux.^2)>1e-1;

% Step 2: correct all those values that are wrong because their respective
% points are in contact.  Note: variables with names ending in c have one
% column for each point that is in contact.

if any(in_ctact)

  % Step 2a: calculate correct values for sticking
  
  n = [0;0;1];
  d = 0;
  vec2 = diag(sqrt(sum(pd(:,in_ctact)'.^2,2)))\pd(:,in_ctact)';

  aux = n'*vec2';
  p_perp = p(:,in_ctact)-n*(n'*p(:,in_ctact));
  p_r = (bsxfun(@times,vec2,((-n'*p(:,in_ctact))./(n'*vec2'))'))'+p(:,in_ctact);
  p_ep = p_r-p_perp;
  
  
  u2 = p_ep(1:end-1,:);
  aux = u(:,in_ctact);
  
  fnc = fn(in_ctact);
  fnc2 = fn(in_ctact);
  udc = pd(1:end-1,in_ctact);
  udc2 = pd(1:end-1,in_ctact);

  zrc = repmat(zr(in_ctact),nd-1,1);
  Kc = K * zrc;
  Dc = D * zrc;
  fKc = Kc .* u(:,in_ctact);

  fKc2 = Kc .* u2;

  ftc  = -fKc - Dc .* udc;		% correct tangent force for sticking
  ftc2 = -fKc2 - Dc .* udc2;

  % now test for slipping

  fslip = mu * fnc;
  if nd == 3				% 3D contact
    ftcmag = sqrt(sum(ftc.^2,1));
    ftcmag2 = sqrt(sum(ftc2.^2,1));
  else					% 2D contact
    ftcmag = abs(ftc);
    ftcmag2 = abs(ftc2);
  end
  fconec = ftcmag ./ fslip;
  slipping = fconec > 1;
  
  fconec2 = ftcmag2 ./ fslip;
  slipping2 = fconec2 > 1;

  % Step 2b: adjust values for those points that are found to be slipping

  if any(slipping)
    attenuator = repmat(fconec(slipping),nd-1,1);
    fts = ftc(:,slipping) ./ attenuator;
    ftc(:,slipping) = fts;
    udc(:,slipping) = -(fts + fKc(:,slipping)) ./ Dc(:,slipping);
  end
  if any(slipping2)
    attenuator = repmat(fconec2(slipping2),nd-1,1);
    fts2 = ftc2(:,slipping2) ./ attenuator;
    ftc2(:,slipping2) = fts2;
    udc2(:,slipping2) = -(fts2 + fKc2(:,slipping2)) ./ Dc(:,slipping2);
  end

  % Step 2c: apply the corrections to the output variables
  
  f(:,in_ctact) = [ftc;fnc];
  ud(:,in_ctact) = udc;
  fcone(in_ctact) = min(2,fconec);
  
  f2(:,in_ctact) = [ftc2;fnc];
  ud2(:,in_ctact) = udc2;
  fcone2(in_ctact) = min(2,fconec2);
  
end

if nargout == 1
  f = [f; ud; fcone];
  f2 = [f2; ud2; fcone2];
end
end
