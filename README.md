## Notifikacni system s hlasovym pruvodcem

### TODO / FIX

1. Vsude je moc zbytecnych sleepu. Jak cekat po prehrani zvuku? Zkousel jsem pouzit vlakna, ale padalo to na necem v pjsipu.

2. Po zaveseni hovoru spadne skript s vyjimkou.

3. Aktualne generuji zvuky rucne pres [festival](https://wiki.archlinux.org/index.php/Festival). Festival vygeneruje wav soubor a jako ho pak prehraju. Idealne pouzit festival API, nebo aspon soubory ukladat do RAM disku.

4. Chtel bych pres (web)socket poslat skriptu povel kam ma volat a jake zvuky ma pouzit. Skript by volani vyridil a vystup (pripadne i DTMF cisla v prubehu) by posilal zpatky socketem. Mohl bych tak snadno skript integrovat do jinych app.

5. Zjistit/zkusit, jestli je mozne z jednoho SIP uctu mit treba 10 soubeznych hovoru. Pripadne nejak vyresit.

6. Cele je to osklive, hlavne ty globalni promenne.


