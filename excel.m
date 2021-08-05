i1 = csvread('input_test1.csv');
o1 = csvread('output_test1.csv');
i2 = csvread('input_test1flip.csv');
o2 = csvread('output_test1flip.csv');

i3 = csvread('input_test2.csv');
o3 = csvread('output_test2.csv');
i4 = csvread('input_test2flip.csv');
o4 = csvread('output_test2flip.csv');

i5 = csvread('input_test3.csv');
o5 = csvread('output_test3.csv');
i6 = csvread('input_test3flip.csv');
o6 = csvread('output_test3flip.csv');

i7 = csvread('input_test4.csv');
o7 = csvread('output_test4.csv');
i8 = csvread('input_test4flip.csv');
o8 = csvread('output_test4flip.csv');

i9 = csvread('input_test5.csv');
o9 = csvread('output_test5.csv');
i10 = csvread('input_test5flip.csv');
o10 = csvread('output_test5flip.csv');

ii = [i1;i2;i3;i4;i5;i6;i7;i8;i9;i10];
oo = [o1;o2;o3;o4;o5;o6;o7;o8;o9;o10];

%iii = ii((1:100:271597),:);
%ooo = oo((1:100:271597),:);
