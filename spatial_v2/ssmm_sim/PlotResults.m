res = squeeze(xout);
force = squeeze(Fout1);
force2 = squeeze(Fout);

% force3 = squeeze(Fout3);
%%


model.camera.body = 7;
model.camera.direction = [1 1 1] ;    
model.camera.locus = [0 0];
model.camera.zoom = 0.5; 

Draw_End_Effector;
showmotion(model,tout,[fbanim(xout);squeeze(xout(14:20,:,:))])
%%
figure(3);
plot(tout,res(11,:)) % plots the longitudinal velocity of the mobile
                     % base
xlabel('Time [s]')
ylabel('Mobile base longitudinal velocity [m/s]')

%%                     
figure(4);
plot(tout,res(5,:))  % plots the longitudinal displacement of the mobile base
xlabel('Time [s]')
ylabel('Mobile base longitudinal displacement [m]')

%%
figure(5);
plot(tout,res(18,:))  % plots the angular position of the arm's first joint
xlabel('Time [s]')
ylabel('Arm Joint 1 Angle [°]')

%%      
figure(6);
plot(tout,res(23,:))  % plots the longitudinal displacement of the mobile base
xlabel('Time [s]')
ylabel('Arm Joint 1 Angular Velocity [°/s]')

%%
figure(7);
cp_force = squeeze(force2(6,:,:));
subplot(2,2,1)
plot(tout,cp_force([CP_Wheel_1_Index:CP_Wheel_2_Index-2],:)')%Rueda 1
xlabel('Time [s]')
ylabel('Wheel 1 Contact Force [N]')
subplot(2,2,2)
plot(tout,cp_force([CP_Wheel_2_Index:CP_Wheel_3_Index-2],:)')%Rueda 2
xlabel('Time [s]')
ylabel('Wheel 3 Contact Force [N]')
subplot(2,2,3)
plot(tout,cp_force([CP_Wheel_3_Index:CP_Wheel_4_Index-2],:)')%Rueda 3
xlabel('Time [s]')
ylabel('Wheel 4 Contact Force [N]')
subplot(2,2,4)
plot(tout,cp_force([CP_Wheel_4_Index:CP_Wheels_Final_Index-1],:)')%Rueda 4
xlabel('Time [s]')
ylabel('Wheel 4 Contact Force [N]')
%%
figure(8);
cp_force = squeeze(force2(6,:,:));
plot(tout,sum(cp_force([CP_Wheel_1_Index:CP_Wheels_Final_Index],:)',2))
xlabel('Time [s]')
ylabel('Total Wheel 1 Contact Force [N]')

break;

%% Analysis of other resuts
% load('Linea_Recta_16CP.mat','Fout');
% load('Linea_Recta_16CP.mat','tout');
% F1=Fout;
% T1=tout;
load('Linea_Recta_32CP_2.mat','Fout');
load('Linea_Recta_32CP_2.mat','tout');
F2=Fout;
T2=tout;
load('Linea_Recta_64CP_2.mat','Fout');
load('Linea_Recta_64CP_2.mat','tout');
F3=Fout;
T3=tout;
load('Linea_Recta_128CP_2.mat','Fout');
load('Linea_Recta_128CP_2.mat','tout');
F4=Fout;
T4=tout;

% N1 = squeeze(F1(6,:,:));
N2 = squeeze(F2(6,:,:));
N3 = squeeze(F3(6,:,:));
N4 = squeeze(F4(6,:,:));
%%
% plot(T1,sum(N1(:,:)',2),'g','linewidth',2)
hold on
plot(T2,sum(N2(:,:),1),'b','linewidth',2)
plot(T3,sum(N3(:,:),1),'k','linewidth',2)
plot(T4,sum(N4(:,:),1),'r','linewidth',2)
xlim([3.5 6])
%%
a = 2000;
plot(sum(N2(:,a:end-1000)',2))
mean(sum(N2(:,a:end-1000)',2))
%%
a2 = sum(N2(:,:),1);
a3 = sum(N3(:,:),1);
a4 = sum(N4(:,:),1);


%%
% for i = 1:length(T2)-1
% time2(i) = T2(i+1)-T2(i);
% 
% end
clear aa2 aa3 aa4 tt2;
tt2(1) = 0;
te = 5e-5;
for i = 2:9.5/te
tt2(i) = tt2(i-1) + te;
[aux2, pos2] = min(abs(tt2(i)-T2));
[aux3, pos3] = min(abs(tt2(i)-T3));
[aux4, pos4] = min(abs(tt2(i)-T4));
aa2(i) = a2(pos2);
aa3(i) = a3(pos3);
aa4(i) = a4(pos4);
end
%%
hold on
plot(tt2,aa2,'b','linewidth',2)
plot(tt2,aa3,'k','linewidth',2)
plot(tt2,aa4,'r','linewidth',2)
xlim([3.5 6])

%%
aux2 = 7000;
L = 19000-aux2;
Fs = 1/te;
NFFT = 2^nextpow2(L); % Next power of 2 from length of y
Y2 = fft(aa2(aux2:end),NFFT)/L;
%Y2 = fft(aa2(aux2:end));
Y3 = fft(aa3(aux2:end),NFFT)/L;
%Y3 = fft(aa3(aux2:end));
Y4 = fft(aa4(aux2:end),NFFT)/L;
%Y4 = fft(aa4(aux2:end));
f2 = Fs/2*linspace(0,1,NFFT/2+1);

% Plot single-sided amplitude spectrum.
plot(f2,2*abs(Y2(1:NFFT/2+1)),'b','linewidth',2) 
hold on
plot(f2,2*abs(Y3(1:NFFT/2+1)),'g','linewidth',2) 
plot(f2,2*abs(Y4(1:NFFT/2+1)),'r','linewidth',2)
hold off
title('Single-Sided Amplitude Spectrum of y(t)')
xlabel('Frequency (Hz)')
ylabel('|Y(f)|')

legend('32 CP', '64 CP', '128 CP');
%xlim([0 200])
%ylim([0 3e8])
grid on

%%
laF=force2(:,end,end);
laPos = PosVel(:,end,1);

%%
plot(tout,force(1:4,:),'linewidth',1)


%%
clear pv1 pv2 pv3 pv4
v_aux = 4;


pv1 = squeeze(PosVel(v_aux,CP_Wheel_1_Index:CP_Wheel_2_Index-1,:));
pv2 = squeeze(PosVel(v_aux,CP_Wheel_2_Index:CP_Wheel_3_Index-1,:));
pv3 = squeeze(PosVel(v_aux,CP_Wheel_3_Index:CP_Wheel_4_Index-1,:));
pv4 = squeeze(PosVel(v_aux,CP_Wheel_4_Index:CP_Wheels_Final_Index,:));

pv5 = squeeze(PosVel(v_aux,1,:));
pv6 = squeeze(PosVel(v_aux,2,:));
pv7 = squeeze(PosVel(v_aux,3,:));
pv8 = squeeze(PosVel(v_aux,4,:));

%%
plot([pv1(65,:); pv2(65,:); pv3(65,:); pv4(65,:)]')
%%
plot([Xup*pv5' pv6 pv7 pv8])
%%
plot([pv1(1,:); pv2(62,:)]')
%%
subplot(2,2,1)
plot(tout,res(19,:)) % plots the arm position
subplot(2,2,2)
plot(tout,res(20,:)) % plots the arm position
subplot(2,2,3)
plot(tout,res(21,:)) % plots the arm position
subplot(2,2,4)
plot(tout,res(22,:)) % plots the arm position


%%

model.appearance.body{7} = { 'colour', [0.1 0.9 0.1],...
                             'facets', 32,...
                             'cyl', [0 -T/2 0; 0 T/2 0], R,...
                             'colour', [0.8 0.1 0.1],...
                             'cyl', [0 -T/2-2e-3 -0.3; 0 T/2+2e-3 -0.3],0.05};
                         
model.appearance.body{8} = { 'colour', [0.1 0.1 0.9],...
                             'facets', 32,...
                             'cyl', [0 -T/2 0; 0 T/2 0], R,...
                             'colour', [0.8 0.1 0.1],...
                             'cyl', [0 -T/2-2e-3 -0.3; 0 T/2+2e-3 -0.3],0.05};

model.appearance.body{9} = { 'colour', [0.9 0.1 0.1],...
                             'facets', 32,...
                             'cyl', [0 -T/2 0; 0 T/2 0], R,...
                             'colour', [0.8 0.1 0.1],...
                             'cyl', [0 -T/2-2e-3 -0.3; 0 T/2+2e-3 -0.3],0.05};
                         
model.appearance.body{10} = { 'colour', [0.1 0.9 0.9],...
                             'facets', 32,...
                             'cyl', [0 -T/2 0; 0 T/2 0], R,...
                             'colour', [0.8 0.1 0.1],...
                             'cyl', [0 -T/2-2e-3 -0.3; 0 T/2+2e-3 -0.3],0.05};