function error = End_Effector_Position_Error(x, model, qn, r, referencia)

Xa{6} = plux( rq(qn), r );

q(1) = x(1);
q(2) = x(2);
q(3) = x(3);

for i = 11:model.NB
[ XJ, S ] = jcalc( model.jtype{i}, q(i-10) );
Xup = XJ * model.Xtree{i};
Xa{i} = Xup * Xa{model.parent(i)};
end

X = inv(Xa{i});                         % xform body i -> abs coords
iset = model.gc.body == i;              % set of points assoc with body i
pt = Xpt( X, model.gc.point(:,iset) );	% xform points to abs coords


pos_extremo = pt;
error = abs(pos_extremo - referencia);
end
