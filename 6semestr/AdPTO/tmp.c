#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#define N 0
#define E 1
#define S 2
#define W 3
int h = 0;
int w = 0;
int n = 0;
int crystals = 0;
char **tab;

char l1 ='\\';
int l11[4] = {3, 2, 1, 0};
char l2 = '/';
int l22[4] = {1,0,3,2};
/*

        N = 0
    W=3       E=1
        S=2
        */
int getone(int *x, int var){
    int c;
    int k=1000;
    while ((c = getchar()) != var){
        *x += (c-'0')*k/10;
        k/=10;
    }
    if( k == 0){
        return 1;
    }
    *x/=k;
    if( *x > 100){
        return 1;
    }
    return 0;
}
int getrest(char** arr){
    int c;
    int i = 0;
    int j = 0;
    while ((c = getchar()) != EOF){
        if(c == '\n'){
            j++;
            i=0;
            continue;
        }
        arr[j][i] = (char)c;
        if((char)c == '*')
            crystals ++;
        i++;

    }
    return 0;
}
void print_result(){
    printf("%d %d\n%d\n", h, w, n);
    for (int i = 0; i <  h; i++){
      for (int j = 0; j < w; j++){
         printf("%c", tab[i][j]);
      }
      printf("\n");
    }
}
int sumof(int num){
    int sum = 0;
    int t=0;
    int i =1;
    int j =0;
    int dir = 1;
/*

        N = 0
    W=3       E=1
        S=2
        */
    //printf("HERE");
    //print_result();
    //printf("\n");
    while(tab[i][j] != '#'){
        if(tab[i][j]==l1){
            dir = l11[dir];
            t++;
        }
        if(tab[i][j]==l2){
            dir = l22[dir];
            t++;
        }
        if(tab[i][j]=='*'){
            sum++;
            tab[i][j]='t';
        }
        if(dir == E){
            j++;
            }
        if(dir == W){
            j--;
            }
        if(dir == N){
            i--;
            }
        if(dir == S){
            i++;
        }

        if(i<0 || i>=h || j<0 || j>=w)

            break;
        //printf("%d %d DIR:%d \n", i, j, dir);
    }
    for (int i = 0; i <  h; i++){
      for (int j = 0; j < w; j++){
         if(tab[i][j]=='t')
            tab[i][j]='*';
      }
    }
    if(t==num)
        return sum;
    else
        return -1;
/*
    if(dir%2==0){
        if(dir==0)
            kier = -1;
        for(int k= i; k<h&& k>=0; k+=kier){
            if(tab[k][j]=='#')
                break;
            if(tab[k][j]=='*')
                sum++;
        }
    }

    else{
        if(dir==3)
            kier = -1;
        for(int k= j; k<w && k>=0; k+=kier){
            if(tab[i][k]=='#')
                break;
            if(tab[i][k]=='*')
                sum++;
        }
    }
*/
}
bool recur_moster(int i, int j, int num, int dir, int suma){
    int starti = i;
    int startj = j;
    int sum = sumof(num);

    if(crystals == sum){
        return true;
    }
    if(sum == -1)
        return false;
    if(sum==suma){
    while(true){

    if(num == n || i>=h || j>=w || i<0 || j<0)
        return false;
    if(tab[i][j]=='#')
        return false;
   // if(tab[i][j]=='*'){
  //      done++;
   // }
    if(tab[i][j]==' '){
        tab[i][j] = l1;
        if(recur_moster(i, j, num+1,  dir, sum))
            return true;
        tab[i][j] = ' ';
        tab[i][j] = l2;
        if(recur_moster(i, j, num+1,  dir,sum))
            return true;
        tab[i][j] = ' ';


    }
    if(tab[i][j]==l1)
        dir = l11[dir];
    if(tab[i][j]==l2)
        dir = l22[dir];
/*

        N = 0
    W=3       E=1
        S=2
        */
    if(dir == E){
        j++;
    }
    if(dir == W){
        j--;
    }
    if(dir == N){
        i--;
    }
    if(dir == S){
        i++;
    }
    }}
    else{

    while(true){

    if(i>=h || j>=w || i<0 || j<0)
        return false;
    if(tab[i][j]=='#')
        break;
    if(tab[i][j]==l1)
        dir = l11[dir];
    if(tab[i][j]==l2)
        dir = l22[dir];
/*

        N = 0
    W=3       E=1
        S=2
        */
    if(dir == E){
        j++;
    }
    if(dir == W){
        j--;
    }
    if(dir == N){
        i--;
    }
    if(dir == S){
        i++;
    }
    }
   // if(tab[i][j]=='*'){
  //      done++;
   // }
   while(true){
    if(tab[i][j]==' '){
        tab[i][j] = l1;
        if(recur_moster(i, j, num+1,  dir, sum))
            return true;
        tab[i][j] = ' ';
        tab[i][j] = l2;
        if(recur_moster(i, j, num+1,  dir,sum))
            return true;
        tab[i][j] = ' ';


    }
    if(n==num || i>=h || j>=w || i<0 || j<0)
        return false;
    if(starti==i && startj ==j)
        return false;
    if(tab[i][j]==l1)
        dir = l11[dir];
    if(tab[i][j]==l2)
        dir = l22[dir];
/*

        N = 0
    W=3       E=1
        S=2
        */
    if(dir == E){
        j--;
    }
    if(dir == W){
        j++;
    }
    if(dir == N){
        i++;
    }
    if(dir == S){
        i--;
    }


   }

    }

}
int main( void)  {




    if(getone(&h,' ')==1){
        printf("Height over 100\n");
        exit(1);
    }
        if(getone(&w,'\n')==1){
        printf("Wight over 100\n");
        exit(1);
    }
        if(getone(&n,'\n')==1){
        printf("Mirrors number over 100\n");
        exit(1);
    }
    tab = (char **) malloc(h*sizeof(char*));
    for (int i=0; i<h; i++){
        tab[i] = (char *) malloc(w*sizeof(char));
    }
    getrest(tab);
    //printf("%d\n" ,crystals);
     /* int i = 1;
    int j = 0;

        N = 0
    W=3       E=1
        S=2
    int di = 1;*/
    if(!recur_moster(1,0,0,1,0))
        printf("ERROR!");
    print_result();

    //printf("%d %d", hw[0], hw[1] );

getchar();
}
