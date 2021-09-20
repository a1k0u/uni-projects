format short;
clc;

eps = 1e-12;
step = 0.1;
x = -pi:0.1:2*pi;
titles = {'f(x) = 2x^4 - 8x^3 + 8x^2 - 1', 'f(x) = 2arctg(x) - x + 3', 'f(x) = 1 + e^{(-x)}'};
colors = {'r', 'g', 'b', 'y'};

count_func = size(titles);

for j=1:count_func(2)
    am_dicho = 0; am_hord = 0;
    
    subplot(count_func(2), 1, j);
    colors_size = size(colors);
    const = mod(j, colors_size(2));
    if const == 0
        const = const + 1;
    end
    color = colors{const};
    plot(x, f(x, j), color);
    hold on;
    grid on;
    
    titles_count = size(titles);
    title(titles{j});
    
    solutions = search_solutions(x, j);
    size_sol = size(solutions);
    
    testing = 1;
    
    size_x = size(x);
    
    for i=1:size_sol(1)
        [root_dicho, iter_dich] = dichotomy(solutions(i, 1), ...
                                           solutions(i, 2), eps, j);
        [root_hord, iter_hord] = hord(solutions(i, 1), ... 
                                      solutions(i, 2), eps, j);
        
        myfunc = @(x, j) f(x, j); % parameterized function
        fun = @(x) myfunc(x, j); % function of x alone
        fzero_ = fzero(fun,  [solutions(i, 1) solutions(i, 2)]);

        plot(root_dicho, f(root_dicho, j), 'x');
        plot(root_hord, f(root_hord, j), '+');
        plot(fzero_, f(fzero_, j), 's');
        
        am_dicho = am_dicho + iter_dich;
        am_hord = am_hord + iter_hord;
        
        if not(int16(root_hord) == int16(root_hord) && ...
                                    int16(root_hord) == int16(fzero_))
            testing = 0;
        end
    end
    fprintf('\nFunction - %s.\n', titles{j});
    fprintf('Founded solutions - %d from a = %f to b = %f.\n', size_sol(1), x(1), x(size_x(2)));
    fprintf('Step for tab was %.2f\n', step);
    fprintf('It takes %d iterations with hord method.\n', am_hord);
    fprintf('And %d iterations with dichotomy method.\n', am_dicho);
    
    if am_dicho > am_hord
        fprintf('Hord method made less for %d iterations.\n', am_dicho-am_hord);
    elseif am_dicho < am_hord
         fprintf('Dichotomy method made less for %d iterations.\n', am_hord-am_dicho);
    end
    
    if testing
        test = 'True';
    else
        test = 'False';
    end
    fprintf('Values of dichotomy, hord and root equivalent = %s.\n', test);    
end

function [y] = f(x, num)
    F(1) = {@(x) 2*x.^4-8*x.^3+8*x.^2-1};
    F(2) = {@(x) 2*atan(x) - x+3};
    F(3) = {@(x) 1 - exp(1).^(x)};
    y = F{num}(x);
end 

function [c, iterations] = dichotomy(a, b, eps, num)
    iterations = 0;
    c = 0;
    if f(a, num)*f(b, num) < 0
        c = (a+b)/2;
        while abs(f(c, num)) > eps
            if f(c, num)*f(a, num) > 0
                a = c;
            else
                b = c;
            end
            c = (a+b)/2;
            iterations = iterations + 1;
        end
    end  
end

function [c, iterations] = hord(a, b, eps, num)
    c = a - ((f(a, num))/(f(b, num) - f(a, num)))*(b - a);
    iterations = 0;
    while abs(f(c, num)) > eps
        c = a - ((f(a, num))/(f(b, num) - f(a, num)))*(b - a);
        if f(a, num)*f(c, num) < 0
            b = c;
        else
            a = c;
        end
        iterations = iterations + 1;
    end
end

function [Array] = search_solutions(x, num)
    n = size(x);
    prev_y = 0;
    solutions = 0;
    Array = [];
    for i=1:n(2)
        value = x(1, i);
        y = f(value, num);
        if prev_y*y < 0
            Array = [Array; x(1, i-1) value]; %#ok<*AGROW>
            solutions = solutions + 1;
        end
        prev_y = y;
    end
end