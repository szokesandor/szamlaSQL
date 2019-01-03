# OTP szamlaforgalom sqlite adatbázisba
Copyright (C) 2019 [SZŐKE, Sándor](mailto:mail@szokesandor.hu)

Azért készült, hogy az OTP internetbank által xls-be exportált havi(!) számlaforgalmat be lehessen emelni (sqlite) adatbázisba. Ezzel könnyebben kezelhetőbbé válik a forgalom elemzése. 

Első körben javasolom az *sqlitebrowser* használatát (amíg nem lesz hozzá valamilyen GUI, ha lesz egyáltalán). Segítségével már könnyen kereshetünk kinek, milyen banszámlára hányszor utaltunk és mekkora összegben időkorlát megadása nélkül. Csak a leleményességünk szab határt, hogy milyen lekérdezést használunk. Pl. havonta mire mennyit költönk...

A program nem tartalmaz sem GUI-t, sem semmilyen kiértékelést, lekérdezést.

### Hasznos hivatkozás:
* [OTP internetbank belépési felület](https://www.otpbank.hu/portal/hu/OTPdirekt/Belepes)
