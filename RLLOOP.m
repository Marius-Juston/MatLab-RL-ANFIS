DE_penalty_gain = 25;
DE_penalty_shape = 1;
reward = 0;
HE_penalty_gain = 25;
HE_penalty_shape = 3;
HE_iwrt_DE = 2;
total_reward = 0;
TDD_reward_gain = 5;
TDD_iwrt_DE = 5;

vel_reward_gain = 1;
vel_iwrt_DE = 1;

steering_penalty_gain = 1;
steering_iwrt_DE = 4;
anfis = 0;
reward_store = zeros(1,100);
distance_error_mean = zeros(1,100);
heading_error_mean = zeros(1,100);
distance_error_max = zeros(1,100);
clock = 0;

count = 0;
for i = 1:100
    if count > 500
        break
    end
    %if mod(i,2) == 0
    %    path(:,2) = -1*path(:,2);
    %end
    sim('SSMM_sim_Torque_3DOF.slx');
    reward_store(i) = sum(rewards_data{6}.Values.Data);
    distance_error_mean(i) = mean(distance_error{1}.Values.Data);
    heading_error_mean(i) = mean(heading_error{1}.Values.Data);
    distance_error_max(i) = max(distance_error{1}.Values.Data);
    save('reward_store', 'reward_store')
    save('distance_error_mean', 'distance_error_mean')
    save('heading_error_mean', 'heading_error_mean')
    save('distance_error_max', 'distance_error_max')
    if i == 1
        plotpath_dyn()
    end
    if i == 10
        plotpath_dyn()
    end
    if i == 20
        plotpath_dyn()
    end
    if i == 30
        plotpath_dyn()
    end
    if i == 37
        plotpath_dyn()
    end
    if i == 40
        plotpath_dyn()
    end
    if i == 50
        plotpath_dyn()
    end
    if i == 60
        plotpath_dyn()
    end
    if i == 80
        plotpath_dyn()
    end
    if i == 100
        plotpath_dyn()
    end
    if i == 120
        plotpath_dyn()
    end
    if i == 140
        plotpath_dyn()
    end
    if i == 160
        plotpath_dyn()
    end
    if i == 180
        plotpath_dyn()
    end
    if i == 200
        plotpath_dyn()
    end
   % if mod(i,2) == 1
   %     testCourse2(16, 5, 6, 6, 6, 1.22, 1, 1.2);
   %     path=[0 0;path];
   % end
   % if mod(i,2) == 0
   %     testCourse3(16, 1.4, 3, 0.8);
   %     path=[0 0;path];
   % end
    %{
    if randi([1 3]) == 1
        testCourse2(16, 5, 6, 6, 6, 1.22, 1, 1.2)
    end
    if randi([1 3]) == 2
        path = [5,   0;
             5,  -5;
             10, -5;
             10, 5;
             15, 5;
             15, 0;
             20, 0];
    end
    if randi([1 3]) == 3
        testCourse3(16, 1.4, 3, 0.8);
    end
    %}
    %{
    if randi([1 4],1) == 1
        testCourse2(16, 5, 6, 6, 6, 1.22, 1, 1.2)
    end
    if randi([1 4],1) == 2
        path = [5,   0;
             5,  -5;
             10, -5;
             10, 5;
             15, 5;
             15, 0;
             20, 0];
    end
    if randi([1 4],1) == 3
        testCourse3(16, 1.4, 3, 0.8);
    end
    if randi([1 4],1) == 4
        path = [      0         0;
   7.7800         0;
   8.6427   -0.3573;
   9.0000   -1.2200;
   9.0000   -4.7800;
   8.6427   -5.6427;
   7.7800   -6.0000;
   1.2200   -8.0000;
   0.3573   -9.3573;
   0.0000   -10.2200;
   0.0000  -10.7800;
   -0.3573  -11.6427;
   -1.2200  -12.0000;
   -3.7800  -12.0000;
   -4.6427  -11.6427;
   -5.0000  -10.7800;
   -5.0000   -1.2200;
   -4.6427   -0.3573;
   -3.7800         0;
   0 0];
    end
    %}
    
    i
    count
end
%{
path = [5,   0;
             5,  -5;
             10, -5;
             10, 5;
             15, 5;
             15, 0;
             20, 0];
sim('SSMM_sim_Torque_3DOF.slx');
plotpath_dyn()
testCourse3(16, 1.4, 3, 0.8);
sim('SSMM_sim_Torque_3DOF.slx');
plotpath_dyn()
testCourse2(16, 5, 6, 6, 6, 1.22, 1, 1.2);
sim('SSMM_sim_Torque_3DOF.slx');
plotpath_dyn()
%}
%sim('test.slx')