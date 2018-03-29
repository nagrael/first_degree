function y = GaussianElimination(A,b,n)
%A to macierz nx3
%b to wektor n
%n to rozmiar
%pêtla po wierszach
%bez pivotingu
for r=1:n
%{
    %PIVOTING
    %poszukujemy najwiekszego wyrazu w kolumnie r
    max=abs(A(r,r)); imax=r;
    for i=r+1:n
        if(abs(A(i,r))>max)
            imax=i;
        max=abs(A(i,r));
        end
    end
 %numer wiersza o maksymalnej wartosci w kolumnie r to “imax”
 %zamieniamy wiersze r-ty oraz imax
    for i=r:n
        buff = A(r,i);
        A(r,i)=A(imax,i);
        A(imax,i)=buff;
    end
%}
 %dzielimy wiersz r-ty przez wartosc z przekatnej
    divider=A(r,2);
    A(r,1)=A(r,1)/divider;
    A(r,2)=A(r,2)/divider;
    A(r,3)=A(r,3)/divider;
 %podobnie dla prawej strony
    b(r)=b(r)/divider;
 %robimy 0 ponizej przekatnej (odejmujemy wiersze)
   
 %odejmujemy wiersze i-ty = i-ty - A(i,r)*r-ty / zeruje sie A(r,1)
 if (r<n)
    mult = A(r+1,1);
    A(r+1,1)=A(r+1,1)-mult*A(r,2);
    A(r+1,2)=A(r+1,2)-mult*A(r,3);
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
    x(k,1)=(b(k)-sum)/A(k,2);
end
y = x;

