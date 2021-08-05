function [ Torque ] = WheelsTorque( u )
%Torque calculation

Accelerator = u(1);
Linear = u(2);
Turn = u(3);

Aux = abs(Linear) + abs(Turn);
if(Aux > 1)
    Linear = Linear/Aux;
    Turn = Turn/Aux;
end


Tmax = 1976.4; %Maximum torque that can be given to a wheel

Tmax_applied = Tmax*Accelerator; %The max torque that may be applied, given
                                 %the accelerator position

T_linear = Tmax_applied*Linear;  %Linear Torque applied by the joystick
T_turn = Tmax_applied*85/30*Turn;%Turn Torque applied by the joystick

if(T_turn>Tmax*Turn)
    T_turn = Tmax*Turn;
end

T_aux = abs(T_turn)+abs(T_linear);
if(T_aux>Tmax)
    T_linear = T_linear/T_aux*Tmax;
    T_turn = T_turn/T_aux*Tmax;
end


RTorque = T_linear - T_turn;
LTorque = T_linear + T_turn;

Torque = [RTorque; LTorque];
end


