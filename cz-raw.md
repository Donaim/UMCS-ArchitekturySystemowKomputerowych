`13.03.18` `cz3`

# Dioda

### Przykład 1

![](assets/cz-dioda-1.png)

Prąd nie popłynie bo dioda jest w kierunku zaporowym!

### Przykład 2

![](assets/cz-dioda-2.png)

Prąd popłynie przy czym duży!  
Rezystancja diody jest bardzo mała (wynika z wykresu/wartości progowej) przez co napięcie będzie bardzo duże i najprawdopodobnie dioda po prostu zepsuje się.  


### Przykład 3

Policzyć I obwodu:

![](assets/cz-dioda-3.png)

U[R1] = U - U[D1] = 4.5 V - 1.5 V = 3 V   

(Prawo Oma)  
I = U[D1] / R = 3 V / 3000 $O = 0.001 A = **1 mA**

### Przykład 4

I = 10 mA  
Policzyć R obwodu:

![](assets/cz-dioda-4.png)

U[R1] = U - U[D1] = 12 V - 3 V = 9 V  

(Prawo Oma)  
I = U[R1] / R
    =>
        R = U[R1] / I = 9 V / 10 mA = **900 $O**  

### Przykład 5

Policzyć opór w obwodzie:  

![](assets/cz-dioda-5.png)

**W połączeniu szeregowym kolejność nie ma znaczenia!**  

![](assets/cz-dioda-5-2.png)

Diody w takim układzie mogą być połączone i to efektywnie nie zmieni niczego.  

![](assets/cz-dioda-5-3.png)

**Diody rozmieszczone równolegle mogą być zastąpione przez jedną o mniejszym napięciu progowym!**

![](assets/cz-dioda-5-4.png)  

Dalsze kroki są banalne.
Odpowiedź: 13k $O

### Przykład 6

Policzyć opór w obwodzie:  
![](assets/cz-dioda-6.png)  

Zauważamy, że D3 jest w zaporowa. Możemy ją wytrzeć.  
Dalsze postępowanie jest analogiczne do przykładu 5.  
Odpowiedź: 13k3 $O

