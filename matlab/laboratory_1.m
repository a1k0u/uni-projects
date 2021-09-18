%dihotomia(1, 2, 3);
%hord(1, 2, 3);
%search(1, 2, 3);

%f(1, 1);
% считывание функций, вывод информаций на график, вывод нескольких
% графиков, тесты, метод ход

%start = input('start: ');
%stop = input('stop: ');
%step = input('step: ');
%x = start:step:stop;
F(1) = {@(x) x.^2-2};
F(2) = {@(x) cos(x)};
F(3) = {@(x) exp(x)};
F(4) = {@(x) sin(x)};

grid on;
hold on;
format long;
start = f(1, 1);
count_func = size(F);

for j=1:count_func(2)
    x = -pi:0.1:pi;
    plot(x, f(x, j));

    solutions = search_solutions(x, j);
    size_ = size(solutions);
    for i=1:size_(1)
        [root_diho, iter_diho] = dihotomia(solutions(i, 1), solutions(i, 2), 1e-12, j);
        [root_hord, iter_hord] = hord(solutions(i, 1), solutions(i, 2), 1e-12, j);
        k = @(x, j) f(x, j);
        fun = @(x) k(x, j);
        fzero_ = fzero(fun,  [solutions(i, 1) solutions(i, 2)]); 

        plot(root_diho, f(root_diho, j), 'x');
        plot(root_hord, f(root_diho, j), '+');
        plot(fzero_, f(fzero_, j), 's');
    end
end


function [y] = f(x, num)
    global F
    f_ = F{num};
    y = f_(x);
end 

function [c, iterations] = dihotomia(a, b, eps, num)
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
    else
        fprintf('Wrong a and b!\n');
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
    fprintf('hord iter=%d, x=%2.4f \n', iterations, c);

end

function [Arr] = search_solutions(x, num)
    n = size(x);
    previus_f = 0;
    solutions = 0;
    Arr = [];
    for i=1:n(2)
        j = x(1, i);
        if previus_f*f(j, num) < 0
            Arr = [Arr; x(1, i-1) j];
            solutions = solutions + 1;
            fprintf('Solution #%d - st = %f, fn = %f.\n', solutions, x(1, i-1), j);
        end
        previus_f = f(j, num);
    end
end