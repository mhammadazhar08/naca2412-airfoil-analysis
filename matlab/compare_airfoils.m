clear; clc; close all;

Re    = 6;                                   % Reynolds number, millions
foils = {'naca2412', 'naca0012'};
names = {'NACA 2412', 'NACA 0012'};
cols  = [0.12 0.37 0.75; 0.85 0.51 0.17];    % blue, orange

here    = fileparts(mfilename('fullpath'));
dataDir = fullfile(here, '..', 'data', 'polars');
figDir  = fullfile(here, '..', 'figures');

figure('Name', 'Airfoil comparison', 'Position', [100 100 1100 800]);
fprintf('%-28s %12s %12s\n', sprintf('Re = %d million', Re), names{:});
results = zeros(6, 2);

for k = 1:2
    T = readtable(fullfile(dataDir, sprintf('%s_polar_Re%dM.csv', foils{k}, Re)));
    a = T.alpha; Cl = T.Cl; Cd = T.Cd; Cm = T.Cm;
    opts = {'-o', 'MarkerSize', 3, 'Color', cols(k,:), 'DisplayName', names{k}};

    subplot(2,2,1); hold on; plot(a, Cl, opts{:});
    subplot(2,2,2); hold on; plot(Cd, Cl, opts{:});
    subplot(2,2,3); hold on; plot(a, Cl./Cd, opts{:});
    subplot(2,2,4); hold on; plot(a, Cm, opts{:});

    lin = a >= -4 & a <= 6;
    p   = polyfit(a(lin), Cl(lin), 1);
    [Clmax, iMax] = max(Cl);
    results(:, k) = [p(1); -p(2)/p(1); Clmax; a(iMax); max(Cl./Cd); mean(Cm(lin))];
end

labels = {'Lift slope (per deg)', 'Zero-lift angle (deg)', 'Cl,max', ...
          'Stall angle (deg)', 'Best Cl/Cd', 'Cm (c/4)'};
for r = 1:numel(labels)
    fprintf('%-28s %12.4f %12.4f\n', labels{r}, results(r,1), results(r,2));
end

titles = {'Lift curve', 'Drag polar', 'Lift-to-drag ratio', 'Pitching moment (c/4)'};
xl     = {'\alpha (deg)', 'C_d', '\alpha (deg)', '\alpha (deg)'};
yl     = {'C_l', 'C_l', 'C_l / C_d', 'C_m'};
for s = 1:4
    subplot(2,2,s); grid on; box on; yline(0, 'k-', 'HandleVisibility', 'off');
    title(titles{s}); xlabel(xl{s}); ylabel(yl{s}); legend('Location', 'best');
end
subplot(2,2,2); xlim([0 0.04]);
sgtitle(sprintf('NACA 2412 vs NACA 0012 - Re = %d million, M = 0.2, N_{crit} = 9', Re));
exportgraphics(gcf, fullfile(figDir, sprintf('compare_matlab_Re%dM.png', Re)), 'Resolution', 200);
