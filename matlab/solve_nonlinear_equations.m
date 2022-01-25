format short;
clc;

main();

function [y] = f(x, num)
    F = {@(x) 2*x.^4-8*x.^3+8*x.^2-1;
         @(x) 2*atan(x) - x+3;
         @(x) (x.^3-0.25.*x.^4+0.125).^(1/2);
         @(x) 2*atan(x) + 3};
    y = F{num}(x);
end 

function [y] = df(x, num, h)
    y = (f(x + h, num) - f(x, num)) / h;
end

function [] = main()
    eps = 1e-12;
    round_num = 3;
    step = 0.001;
    x = -2*pi:step:2*pi;
    titles = {'f(x) = 2x^4 - 8x^3 + 8x^2 - 1', 'f(x) = 2arctg(x) - x + 3'};
    colors = {'r', 'g', 'b'};
    method = {@dichotomy; @hord; @newton; @iteration};

    count_func = size(titles);

    for j=1:count_func(2)
        subplot(count_func(2), 1, j);

        colors_size = size(colors);
        const = mod(j, colors_size(2));
        if const == 0
            const = const + 1;
        end
        color = colors{const};

        plot(x, f(x, j), color);
        hold on; grid on;

        title(titles{j});
        xlabel('Ox');
        ylabel('Oy');

        solutions = search_solutions(x, j);
        size_sol = size(solutions);

        testing = 1;

        size_x = size(x);
        counter_iterations = {0; 0; 0; 0};

        for i=1:size_sol(1)
            for k=1:4
                if not(k == 4) || i == 1
                    [root_method, iter_method] = method{k}(solutions(i, 1), ...
                                                     solutions(i, 2), eps, j);
                end

                myfunc = @(x, j) f(x, j); % parameterized function
                fun = @(x) myfunc(x, j); % function of x alone
                fzero_ = fzero(fun,  [solutions(i, 1) solutions(i, 2)]);

                plot(root_method, f(root_method, j), 'x');
                plot(fzero_, f(fzero_, j), 's');

                counter_iterations{k} = counter_iterations{k} + iter_method;
                if not(round(root_method, round_num) == round(fzero_, round_num))
                    testing = 0;
                end
                if j == 1
                    root_polynomial = roots([2 -8 8 0 -1]);
                    size_root_pol = size(root_polynomial);
                    if not(round(root_method, round_num) == ...
                            round(root_polynomial(size_root_pol(1)-i+1), round_num))
                        testing = 0;
                    end
                end
                
                if k == 4 && not(i > 1) && not(testing)
                    testing = 1;
                end
            end
        end
        fprintf('\nFunction - %s.\n', titles{j});
        fprintf('Founded solutions - %d from a = %f to b = %f with step - %.2f.\n', ...
                                           size_sol(1), x(1), x(size_x(2)), step);
        fprintf('Iterations: dichotomy - %d, hord - %d, newton - %d, iteration method - %d.\n', ...
                                           counter_iterations{1}, counter_iterations{2}, counter_iterations{3}, counter_iterations{4});
        
        if testing, test = 'True'; else, test = 'False'; end 
        fprintf('Values of dichotomy, hord, newton, iteration and root/fzero equivalent = %s.\n', test);    
    end
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
    iterations = 0;
    if f(a, num)*f(b, num) < 0
        c = a - ((f(a, num))/(f(b, num) - f(a, num)))*(b - a);
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
end

function [x, iterations] = newton(a, b, eps, num)
    iterations = 0;
    if f(a, num)*f(b, num) < 0
        if f(a, num)*df(a, num, 10e-12) > 0
            x = a;
        else
            x = b;
        end
        while abs(f(x, num)) > eps
            x = x - (f(x, num)/df(x, num, 10e-12));
            iterations = iterations + 1;
        end
    end
end

function [c, iterations] = iteration(a, b, eps, num)
    iterations = 0;
    if abs(df(a, num + 2, 10e-12)) < 1 && abs(df(b, num + 2, 10e-12)) < 1
        c = a;
        while abs(f(c, num)) > eps
            c = f(c, num + 2);
            iterations = iterations + 1;
        end
    end
end

function [Array] = search_solutions(x, num)
    n = size(x);
    prev_y = 0;
    Array = [];
    for i=1:n(2)
        value = x(1, i);
        y = f(value, num);
        if prev_y*y < 0
            Array = [Array; x(1, i-1) value]; %#ok<*AGROW>
        end
        prev_y = y;
    end
end
