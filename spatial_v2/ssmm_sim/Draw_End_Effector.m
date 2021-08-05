res = squeeze(xout);

for j = 1:1:length(Arm_Angles)
        
    Xa{6} = plux( rq(res(1:4,j)), res(5:7,j) );

    q(1) = res(18,j);
    q(2) = res(19,j);
    q(3) = res(20,j);

    for i = 11:model.NB
        [ XJ, S ] = jcalc( model.jtype{i}, q(i-10) );
        Xup = XJ * model.Xtree{i};
        Xa{i} = Xup * Xa{model.parent(i)};
    end

    X = inv(Xa{i});                         % xform body i -> abs coords
    iset = model.gc.body == i;              % set of points assoc with body i
    pt = Xpt( X, model.gc.point(:,iset) );	% xform points to abs coords
    pos_endEffector(j,:) = pt;
end

for x = 202:200:length(pos_endEffector)

        model.appearance.base = ...
        {model.appearance.base,...
        'colour', [0.9 0 0], 'line', pos_endEffector(x-200:x,:)};
end

for x = 202:200:length(Reference_Pos)
        model.appearance.base = ...
        {model.appearance.base,...
        'colour', [0 0.9 0], 'line', Reference_Pos(x-200:x,:)};
end