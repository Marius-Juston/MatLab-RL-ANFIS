inputs = fuzzy_input{1}.Values.Data;
%outputs = fuzzy_output{1}.Values.Data;
%csvwrite('input_test5flip.csv',inputs);
%csvwrite('output_test5flip.csv',outputs);
m = mean(abs(inputs(:,1)))
ma = max(abs(inputs(:,1)))