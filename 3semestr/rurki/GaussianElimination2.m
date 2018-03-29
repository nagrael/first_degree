function y = GaussianElimination2(A,b,n)
%A to macierz nx4 potrzebne do pivotingu
%b to wektor n
%n to rozmiar
%pêtla po wierszach
%z pivotingem

for r=1:n


    %PIVOTING
    %poszukujemy najwiekszego wyrazu w kolumnie r/ moze byc tylko w A(r,2)
if(r<n)
    max=abs(A(r,2)); imax=r;
        if(abs(A(r+1,1))>max)
            imax=r+1;
        end

 %numer wiersza o maksymalnej wartosci w kolumnie r to “imax”
 %zamieniamy wiersze r-ty oraz imax
    if(r~=imax)
        buff = b(r);
        b(r) = b(imax);
        b(imax) = buff;
        for i=1:3
            buff = A(r,i+1);
            A(r,i+1) = A(imax,i);
            A(imax,i) = buff;
        end
        
    end
end
 %dzielimy wiersz r-ty przez wartosc z przekatnej
    divider=A(r,2);
    if(divider~=0)
  
    for i=1:4
    A(r,i)=A(r,i)/divider;
    end
 %podobnie dla prawej strony
    b(r)=b(r)/divider;
    end
 %robimy 0 ponizej przekatnej (odejmujemy wiersze)

 %odejmujemy wiersze i-ty = i-ty - A(i,r)*r-ty / zeruje sie A(r,1)
 
 if (r<n)
    mult = A(r+1,1);
    for i=1:3
    A(r+1,i)=A(r+1,i)-mult*A(r,i+1);
    end
    b(r+1)=b(r+1)-mult*b(r);
 end

end

%w tym miejscu mamy macierz trojkatna gorna
%rozwiazujemy uklad rownan zaczynajac od ostatniego
   x(n,1)=b(n)/A(n,2);
%petla po rownaniach od przedostatniego do pierwszego
for k=n-1:-1:1
 %dla kazdego rownania, mamy
 % A(k,k)x(k)+A(k,k+1)x(k+1)+...+A(k,n)x(n)=b(n)
  
    sum=A(k,3)*x(k+1,1);
    if(k~=n-1)
    sum=sum+A(k,4)*x(k+2,1);
    end
    x(k,1)=(b(k)-sum)/A(k,2);
end
y = x;

