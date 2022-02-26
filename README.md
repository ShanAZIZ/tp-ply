# TP-PLY 
__AZIZ Shana, BOUBCHIR Marwan__


## Syntaxe


affectation, print :

```
x=4;x=x+3;print(x);
```

affectation élargie, affectation 
```
x=9; x+=4; x++; print(x);
```

conditions if-else : 
```
i=10; if(i>11){ print(2);}else{print(3);};

i=10;if(i>9){print(2);}else{print(3);};
```

while, for 


```
x=4;while(x<30){x=x+3;print(x);}; for(i=0 ;i<4 ;i=i+1){print(i*i);};
```
_attention_ : dans le for, le dernier statement 'i=i+1' ne nécessite pas de ';'. 


#fonctions void avec paramètres s4='fonctionVoid toto(a, b){print(a+b) ;} toto(3, 5) ;’  #fonctions value avec paramètres et return explicite s5='fonctionValue toto(a, b){c=a+b ;return c ;} toto(3, 5) ;’  #fonctions value avec paramètres et return implicite   s5='fonctionValue toto(a, b){c=a+b ; toto=c ;} toto(3, 5) ;’   #fonctions value avec paramètres et return coupe circuit s6='fonctionValue toto(a, b){c=a+b ;return c ; print(666) ;} x=toto(3, 5) ; print(x) ;’  #fonctions value avec paramètres, return coupe circuit et scope des variables s7='fonctionValue toto(a, b){if(a==0) return b ; c=toto(a-1, b-1) ;return c ; print(666) ;} x=toto(3, 5) ; 
print(x) ;’ 








----------------------------------
 incrémentation et affectation élargie : x++, x+=1

