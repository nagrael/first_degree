function [val, iter] = secant(a, b, f, dig, epsilon)
    digits(dig)
    iter = 0;
    %if sign(f(a)) == sign(f(b))
     %   return
    %end
    x0 = sym(a);
    x1 = sym(b);
    tmp = 0;
    while(abs(vpa(f(x1))) > epsilon)
        tmp = x1;
        x1 = vpa(x1 - ((f(x1))*(x1-x0))/(f(x1)-f(x0)));
        x0 = tmp;
        iter = iter +1;
    end
    val = x1;
    iter
    
end