function zadv2 (a,b,c,f,uL,uR,n)

fa = str2func(strcat('@(x)',a));
fb = str2func(strcat('@(x)',b));
fc = str2func(strcat('@(x)',c));
ff = str2func(strcat('@(x)',f));

h=1/n;

function y = P1(x)
    y = ((fa((x+1)*h) - fa((x-1)*h)) / (4 * h^2)) + (fa(x*h))/(h^2) + (fb(x*h) / (2*h));
end   
function y = P2(x)
    y = fc(x*h) - ((2 * fa(x*h)) / h^2);
end 
function y = P3(x)
    y = ((fa((x-1)*h) - fa((x+1)*h)) / (4 * h^2)) + (fa(x*h))/(h^2) - (fb(x*h) / (2*h));
end
% tworzymy tablice o rozmiarze (n-1)x3
macierz = zeros(n-1,4);
% tworzymy wektor funkcji o rozmiarze (n-1)

wektor_pr = zeros(n-1,1);
% tworzymy wektor do przechowywania wynik�w
wynik = zeros(n-1,1);
% wype�nianie macierzy
macierz(1,3) = P1(1);
macierz(1,2) = P2(1);
for k = 2:n-2
 macierz(k,1) = P3(k);
 macierz(k,2) = P2(k);
 macierz(k,3) = P1(k);
end
macierz(n-1,2) = P2(n-1);
macierz(n-1,1) = P3(n-1);
% wype�niamy wektor prawej strony

wektor_pr(1,1) = ff(h) - P3(0)*uL;
wektor_pr(n-1,1) = ff((n-1)*h) - P1(n)*uR;
for k = 2:n-2
 wektor_pr(k,1) = ff(k*h);
end
%{
% eliminacja gausa dla macierzy (n-1)x3 i wektora prawej strony
wektor_pr(1,1) = wektor_pr(1,1)/macierz(1,2);
macierz(1,:) = macierz(1,:)/macierz(1,2);
for k = 2:n-1
  dzielnik = macierz(k,1)/macierz(k-1,2);
  macierz(k,1) = macierz(k,1) - dzielnik * macierz(k-1,2);
  macierz(k,2) = macierz(k,2) - dzielnik * macierz(k-1,3);
  wektor_pr(k,1) = wektor_pr(k,1) - dzielnik * wektor_pr(k-1,1);
  wektor_pr(k,1) = wektor_pr(k,1)/macierz(k,2);
  macierz(k,:) = macierz(k,:)/macierz(k,2);
end
% podstawienie odwrotne po eliminacji gausa
wynik(n-1,1) = wektor_pr(n-1,1);
for k = n-2:-1:1
  wynik(k,1) = wektor_pr(k,1) - macierz(k,3)*wynik(k+1,1);
end
%}

wynik = GaussianElimination2(macierz, wektor_pr, n-1);


% tworzymy wektor punkt�w
punkty = [0:1/n:1];
% oraz wartosci u(xn)
wartosci = zeros(1,n+1);
wartosci(1,1) = uL;
for k = 2:n
 wartosci(k)=wynik(k-1);
end
wartosci(1,n+1) = uR;
p = 3;
x=punkty;
y=wartosci;
% x, y - wektory wsp��rzednych
%p = stopien wielomianu
WA(1:p+1,1:p+1)=0;
WB(1:p+1)=0;
%petla po punktach
for k=1:n
 % petla po wierszach
 for i=1:p+1
 %petla po kolumnach
 for j=1:p+1
 WA(i,j)=WA(i,j)+x(k)^(i+j-2);
 end
 WB(i)=WB(i)+y(k)*x(k)^(i-1);
 end
end
U=WA\WB';
%rysowanie wielomianu aproksymujacego
dokl = 10000;
punkt = [0:1/dokl:1];
%petla po punktach dla ktorych rysujemy wartosci wielomianu
for i=1:dokl+1
 %petla po wspolczynnikach wielomianu
 wielomian(i)=0;
 for j=1:p+1
 wielomian(i)=wielomian(i)+U(j)*punkt(i)^(j-1);
 end
end
plot(punkt,wielomian);
hold on
plot(x,y,'rx');
hold off
end


