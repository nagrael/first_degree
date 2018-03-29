function [val, iter] = bisect(a, b, f, dig, epsilon)
    digits(dig);
    iter = 0;
    %if sign(f(a)) == sign(f(b))
     %   return
    %end
    while(true)
        x1 = vpa((a+b)/2);
        if vpa(f(x1)) == 0 || abs(vpa(b-a))<epsilon
            break
        end
        if sign(vpa(f(x1))) ~= sign(vpa(f(b)))
            a = x1;
        else 
            b = x1;
        end
        iter = iter + 1;
    end
    val = vpa((a+b)/2);
    iter
end
