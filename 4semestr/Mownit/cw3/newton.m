function [val, iter] = newton(a, b, f,df, dig, epsilon)
    digits(dig)
    iter = 0;
    %if sign(f(a)) == sign(f(b))
     %   return
    %end
    x1 = abs((a-b)/2);
    while(abs(vpa(f(x1))) > epsilon)
        x1 = vpa(x1 - vpa(f(x1))/vpa(df(x1)));
        iter = iter +1;
    end
    val = x1;
    iter
    
end