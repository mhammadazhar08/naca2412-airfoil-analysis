clear; clc; close all;

here     = fileparts(mfilename('fullpath'));
cpFile   = fullfile(here, '..', 'data', 'cp', 'cp_Re1M_alpha-4.txt');   % <-- change this
figDir   = fullfile(here, '..', 'figures');

% The export has 6 header lines, then columns: x, Cpi, Cpv, Qi, Qv
d   = readmatrix(cpFile, 'NumHeaderLines', 6, 'FileType', 'text');
x   = d(:,1);
cpi = d(:,2);    % inviscid (no friction)
cpv = d(:,3);    % viscous (with boundary layer) - the real result

% Points run from the trailing edge, over the upper surface to the
% leading edge, then back along the lower surface. Split at the nose.
[~, le] = min(x);
up = 1:le;
lo = le:numel(x);

figure('Position', [100 100 900 550]); hold on; grid on; box on;
plot(x(up), cpv(up), 'b-',  'LineWidth', 2, 'DisplayName', 'Upper surface (viscous)');
plot(x(lo), cpv(lo), 'r-',  'LineWidth', 2, 'DisplayName', 'Lower surface (viscous)');
plot(x(up), cpi(up), 'b--', 'DisplayName', 'Upper (inviscid)');
plot(x(lo), cpi(lo), 'r--', 'DisplayName', 'Lower (inviscid)');
set(gca, 'YDir', 'reverse');            % aerodynamics convention: suction (negative Cp) plotted upward
xlabel('x/c'); ylabel('C_p'); legend('Location', 'southeast');
title('NACA 2412 pressure distribution');

% Check: integrate Cp around the airfoil to recover the normal-force coefficient
xu = flipud(x(up)); cu = flipud(cpv(up));      % upper surface, leading edge -> trailing edge
xl = x(lo);         cl = cpv(lo);              % lower surface, leading edge -> trailing edge
Cn = trapz(xl, cl) - trapz(xu, cu);
fprintf('Normal-force coefficient from Cp integration: Cn = %.3f\n', Cn);
fprintf('(For small angles Cl is approximately Cn.)\n');

exportgraphics(gcf, fullfile(figDir, 'cp_matlab.png'), 'Resolution', 200);
