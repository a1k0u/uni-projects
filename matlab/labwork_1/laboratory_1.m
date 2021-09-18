%dihotomia(1, 2, 3);
%hord(1, 2, 3);
%search(1, 2, 3);

%f(1, 1);
% считывание функций, вывод информаций на график, вывод нескольких
% графиков, тесты, метод ход

%start = input('start: ');
%stop = input('stop: ');
%step = input('step: ');
%x = start:step:stop

F(1) = {@(x) x.^2-2}; 
F(2) = {@(x) exp(x)-5};
F(3) = {@(x) sin(x)};

format long;

eps = 1e-12;

start = f(12, 1);
count_func = size(F);

am_dicho = 0;
am_hord = 0;
for j=1:count_func(2)
    x = -pi:0.1:pi;
    
    subplot(count_func(2), 1, j);
    plot(x, f(x, j));
    hold on;
    grid on;
    
    solutions = search_solutions(x, j);
    size_ = size(solutions);
    for i=1:size_(1)
        [root_dich, iter_dich] = dichotomy(solutions(i, 1), ...
                                           solutions(i, 2), eps, j);
        [root_hord, iter_hord] = hord(solutions(i, 1), ... 
                                      solutions(i, 2), eps, j);
        
        myfunc = @(x, j) f(x, j); % parameterized function
        fun = @(x) myfunc(x, j); % function of x alone
        fzero_ = fzero(fun,  [solutions(i, 1) solutions(i, 2)]); 

        plot(root_dich, f(root_dich, j), 'x');
        plot(root_hord, f(root_hord, j), '+');
        plot(fzero_, f(fzero_, j), 's');
        
        am_dicho = am_dicho + iter_dich;
        am_hord = am_hord + iter_hord;
    end
%     info = legend('Solutions on this gap - %d\n', size_(1));
%     set(info, 'Location', 'NorthWest');
end

function [y] = f(x, num)
    F(1) = {@(x) x.^2-2}; 
    F(2) = {@(x) exp(x)-5};
    F(3) = {@(x) sin(x)};
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