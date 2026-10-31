
clear; clc; close all;

here     = fileparts(mfilename('fullpath'));          % folder this script is in
dataDir  = fullfile(here, '..', 'data', 'polars');
figDir   = fullfile(here, '..', 'figures');

Re_list = [1 3 6 9];               % Reynolds numbers, in millions
colors  = lines(numel(Re_list));   % one colour per Reynolds number

figure('Name','NACA 2412 polars','Position',[100 100 1100 800]);

for k = 1:numel(Re_list)
    R = Re_list(k);
    T = readtable(fullfile(dataDir, sprintf('naca2412_polar_Re%dM.csv', R)));   % load the data

    alpha = T.alpha;   % angle of attack (degrees)
    Cl    = T.Cl;      % lift coefficient
    Cd    = T.Cd;      % drag coefficient
    Cm    = T.Cm;      % pitching moment coefficient (about quarter chord)
    label = sprintf('Re = %d million', R);

    subplot(2,2,1); hold on; plot(alpha, Cl, '-o', 'MarkerSize', 3, 'Color', colors(k,:), 'DisplayName', label);
    subplot(2,2,2); hold on; plot(Cd, Cl,    '-o', 'MarkerSize', 3, 'Color', colors(k,:), 'DisplayName', label);
    subplot(2,2,3); hold on; plot(alpha, Cl./Cd, '-o', 'MarkerSize', 3, 'Color', colors(k,:), 'DisplayName', label);
    subplot(2,2,4); hold on; plot(alpha, Cm, '-o', 'MarkerSize', 3, 'Color', colors(k,:), 'DisplayName', label);

    % ---- Key numbers for the report ----
    lin = alpha >= -4 & alpha <= 6;              % straight part of the lift curve
    p   = polyfit(alpha(lin), Cl(lin), 1);       % fit a straight line: Cl = slope*alpha + c
    [Clmax, iMax] = max(Cl);
    [LDmax, iLD]  = max(Cl./Cd);
    fprintf('Re = %d million\n', R);
    fprintf('  Lift slope        = %.4f per degree\n', p(1));
    fprintf('  Zero-lift angle   = %.2f deg\n', -p(2)/p(1));
    fprintf('  Cl_max            = %.3f at %.1f deg (stall)\n', Clmax, alpha(iMax));
    fprintf('  Minimum Cd        = %.5f\n', min(Cd));
    fprintf('  Best Cl/Cd        = %.1f at %.1f deg\n\n', LDmax, alpha(iLD));
end

% Thin-airfoil theory line for comparison: Cl = 2*pi*(alpha - alpha_L0), alpha in radians
subplot(2,2,1);
a = -5:0.5:12;
plot(a, 2*pi*deg2rad(a + 2.08), 'k--', 'DisplayName', 'Thin-airfoil theory');

titles = {'Lift curve','Drag polar','Lift-to-drag ratio','Pitching moment (c/4)'};
xl     = {'\alpha (deg)','C_d','\alpha (deg)','\alpha (deg)'};
yl     = {'C_l','C_l','C_l / C_d','C_m'};
for s = 1:4
    subplot(2,2,s); grid on; box on;
    title(titles{s}); xlabel(xl{s}); ylabel(yl{s});
    legend('Location','best');
end
sgtitle('NACA 2412 - XFLR5 results, M = 0.2, N_{crit} = 9');

exportgraphics(gcf, fullfile(figDir, 'polars_all_Re_matlab.png'), 'Resolution', 200);
