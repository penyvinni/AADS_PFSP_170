close all, clear, clc;

% NEH Algorithm O(n^3m)
neh_makespan = [699 897 692 879 742 750 782 743 782 631 1104 1287 1014 913 1096 1038 950 1082 1124 1086];

% Tabu Search Algorithm
tabu_makespan = [522 721 532 710 533 687 614 633 607 470 640 710 587 542 616 611 625 563 666 665];


% Plot for NEH vs Tabu
figure;
plot(neh_makespan, 'r*-', 'LineWidth', 1, 'DisplayName', 'NEH');
hold on;
plot(tabu_makespan, 'b*-', 'LineWidth', 1, 'DisplayName', 'Tabu');
title('NEH vs Tabu Search Makespans');
xlabel('Time');
ylabel('Makespan');
grid on;
legend('NEH','Tabu Search');
