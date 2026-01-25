clear; 
clc;

%tx_data     = fi([1:1:1000], 0, 8, 0);

%x = 5775348759348742188734095349580;
%x=4441;

tx_data     = fi([1:1:1000], 0, 8, 0);
 x=zeros(1, 1024);
 for i=1:1024
     x(i) = randi([4441612681297957 4441612681697957]); %52-53 bits -- randi() not allowing imax and imin more than 2^53
 end
 
 d = 64;  % initial delay added for pps 
 as = 8; % delay added in AddSub block 