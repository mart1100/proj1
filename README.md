# Transformacje geodezyjne

## Spis treści 
* [Ogólne informacje](#ogólne-informacje)
* [Wymagania sprzętowe](#wymagania-sprzętowe)
* [Funkcje](#funkcje)
* [Flagi](#flagi)
* [Uruchomienie programu](#uruchomienie-programu)
* [Przykłady użycia](#przykłady-użycia)
* [Znane błędy](#znane-błędy)

## Ogólne informacje
Celem programu jest transformacja współrzędnych geocentrycznych z pliku (X,Y,Z), między danymi układami współrzędnych geodezyjnych i ortokartezjańskich. Ten program umożliwia przeliczenie: współrzędnych ortokartezjaśkich na współrzedne geodezyjne, współrzędnych geodezyjnych (&phi;, &lambda;, h) na ortokartezjańskie, współrzędnych geodezyjnych do układów odniesienia na terenie Polski (PL2000, PL1992). Program obsługuje elipsoidy WGS84, GRS80, i elipsoidę Krasowskiego.
Projekt powstał w celu utrwalenia informacji zdobytych na zajęciach z Informatyki Geodezyjnej.

## Wymagania sprzętowe
Wymagania, które musi spełnić komputer użytkownika:
1. Posiadanie wersji programu [Python 3.8 lub wyższej](https://www.python.org/downloads/).
2. Zainstalowane biblioteki sys, math oraz numpy
3. Dane wejściowe muszą być zapisane w pliku tekstowym.
4. Posiadanie systemu operacyjnego Windows, MacOS lub Linux.

## Funkcje:
Lista funkcji, które oferuje program:
* `xyz2plh` : Wykorzystując algorytm Hirvonena, przelicza współrzędne ortokartezjańskie (x, y, z) na współrzędne geodezyjne (&phi;,&lambda;,h).
* `plh2xyz` : Przelicza współrzędne geodezyjne (phi, lambda, h) na współrzędne ortokartezjańskie (x, y, z).
* `xyzGRS2KRA` : Transformuje współrzędne kartezjańskie - geocentryczne z elipsoidy GRS-80 do układu elipsoidy Krasowskiego
* `xyzKRA2GRS` : Transformuje współrzędne kartezjańskie - geocentryczne z wejściowej elipsoidy Krasowskiego do układu elipsoidy GRS-80
* `pl21992` : Przelicza współrzędne geodezyjne (&phi;,&lambda;,h) do układu 1992.
* `pl22000` : Przelicza współrzędne geodezyjne (&phi;,&lambda;,h) do układu 2000.
* `xyz2neu` : Transformuje współrzędne geocentryczne do układu topocentrycznego.

## Flagi
Lista wywoływalnych flag oferowanych przez program:
* --flags : Wyświetla wszystkie dostępne flagi
* --xyz2plh : Uruchamia funkcję `xyz2plh`
* --plh2xyz : Uruchamia funkcję `plh2xyz`
* --xyzGRS2KRA : Uruchamia funkcję `xyzGRS2KRA`
* --xyzKRA2GRS : Uruchamia funkcję `xyzKRA2GRS`
* --pl21992 : Uruchamia funkcję `pl21992`
* --pl22000 : Uruchamia funkcję `pl22000`
* --xyz2neu : Uruchamia funkcję `xyz2neu`
* --header_lines : Umożliwia pominięcie podanej liczby wierszy nagłówka przy odczytywaniu pliku wejściowego. 
* --model : Umożliwia określenie modelu elipsoidy odniesienia współrzędnych wyjściowych. Program obsługuje elipsoidy WGS84, GRS80 oraz Krasowskiego.
* --dms : Przy użyciu z flagą --xyz2plh zwraca wynik w formacie stopnie,minuty,sekundy


## Uruchomienie programu
Program należy uruchomić za pomocą Command Prompt, Microsoft PowerShell lub Terminal. W Command Center można to zrobić wpisując w wiersz poleceń komendę:
```
python skrypt.py --funkcja --header_lines [liczba_wierszy_naglowka] --model [model_elipsoidy] wsp_inp.txt
```

gdzie w miejscu flagi --funkcja należy wpisać jedną z interesujących nas funkcji programu, a plik tekstowy wsp_inp.txt zawiera nasze współrzędne w postaci (X,Y,Z), (X,Y) lub (&phi;,&lambda;,h) oddzielone przecinkiem.
W miejscu [liczba_wierszy_naglowka] należy wpisać liczbę wierszy nagłówka w pliku wsp_inp.txt. W miejscu [model_elipsoidy] powinien znaleźć się model elipsoidy odniesienia współrzędnych wyjściowych: wgs84, grs80 lub krasowski.
> [!IMPORTANT]
 >Kolejność wpisywania flag ma znaczenie - żeby program działał poprawnie kolejność flag powinna być tylko taka jak w podanych przykładach.

> [!NOTE]
 > W przypadku użycia flagi --xyzGRS2KRA lub --xyzKRA2GRS użycie flagi --model nie da efektu i nie jest konieczne. W przypadku pozostałych funkcji, użycie flagi --model jest wymagane.

## Przykłady użycia
**1. Przeliczanie współrzędnych ortokartezjańskich na współrzędne geodezyjne.** <br/>
Parametrami wejściowymi są:
* X, Y, Z : FLOAT,współrzędne w układzie orto-kartezjańskim

Parametrami wyjściowymi są:
* lat : FLOAT, [stopnie dziesiętne] - szerokość geodezyjna
* lon : FLOAT, [stopnie dziesiętne] - długość geodezyjna
* h : FLOAT, [m] - wysokość elipsoidalna <br/>
Dla przykładowego pliku wejściowego ze współrzędnymi geocentrycznymi 'wsp_inp.txt' w wierszu poleceń należy wpisać komendę:
```
python skrypt.py --xyz2plh --header_lines 4 --model wgs84 wsp_inp.txt
```

W ten sposób w miejscu, w którym zapisany jest plik skrypt.py powstaje plik tekstowy zawierający wyniki tej operacji: result_xyz2plh.txt <br/>
W przypadku, gdy współrzędne w pliku wyjściowym mają być podane w stopniach, minutach, sekundach należy użyć flagi `--dms`:
```
python skrypt.py --xyz2plh --header_lines 4 --model wgs84 --dms wsp_inp.txt
```

**2. Przeliczenie współrzędnych geocentrycznych z układu elipsoidy GRS80 do układu elipsoidy Krasowskiego.** <br/>
Parametrami wejściowymi są:
* x_grs, y_grs, z_grs : FLOAT, [m] - współrzędne geocentryczne dla elipsoidy GRS-80
       
Parametrami wyjściowymi są:
* x_kra, y_kra, z_kra : TUPLE, [m] - współrzędne geocentryczne dla elipsoidy Krasowskiego

Dla przykładowego pliku wejściowego ze współrzędnymi geocentrycznymi GRS80 'wsp_grs_inp.txt' w wierszu poleceń należy wpisać komendę:
```
python skrypt.py --xyzGRS2KRA --header_lines 1 wsp_grs_inp.txt
```
W ten sposób w miejscu, w którym zapisany jest plik skrypt.py powstaje plik tekstowy zawierający wyniki tej operacji: 'result_xyzGRS2KRA.txt'

**3. Przeliczenie współrzędnych geodezyjnych do układu PL1992.** <br/>
Parametrami wejściowymi są:
* phi: FLOAT, [stopnie dziesiętne] - szerokosć geodezyjna
* lam: FLOAT, [stopnie dziesiętne] - długosć geodezyjna
* h: FLOAT, [m] - wysokość elipsoidalna

Parametrami wyjściowymi są:
* x1992 : FLOAT, [m] - odcięta w układzie 1992
* y1992 : FLOAT, [m] - rzędna w układzie 1992

Dla przykładowego pliku wejściowego ze współrzędnymi geodezyjnymi w układzie wgs84 'wsp_plh_inp.txt' w wierszu poleceń należy wpisać komendę:
```
python skrypt.py --pl21992 --header_lines 1 --model wgs84 wsp_plh_inp.txt
```
Następnie należy poprzez wpisanie w konsolę wybrać format współrzędnych w pliku wejściowym: `dec_degrees` dla stopni dziesiętnych, `dms` dla stopni,minut,sekund w postaci dd:mm:ss.ss.

W ten sposób powstaje plik tekstowy zawierający wyniki tej operacji: result_pl21992.txt

> [!IMPORTANT]  
 > Zarówno w funkcji pl21992 jak i w pl22000 jeśli wysokość elipsoidalna punktów h nie jest znana, należy w jej miejsce wpisać 0 w tekstowym pliku wejściowym.

**4. Przeliczenie współrzędnych geodezyjnych do układu NEU.** <br/>
Parametrami wejściowymi są:
* x, y, z : FLOAT, [m] - współrzędne geocentryczne 
* x0, y0, z0 : FLOAT, [m] - współrzędne geocentryczne nowego srodka układu
  
Współrzędnymi wyjściowymi są:
* n, e, u : TUPLE, [m] - współrzędne topocentryczne

Dla przykładowego pliku wejściowego ze współrzędnymi geocentrycznymi 'wsp_inp.txt' oraz x0 = 3664945.620, y0 = 1409150.120, z0 = 5009524.552 w wierszu poleceń należy wpisać komendę:
```
python skrypt.py --xyz2neu --header_lines 4 --model wgs84 3664945.620 1409150.120 5009524.552 wsp_inp.txt
```
W ten sposób powstaje plik tekstowy zawierający wyniki tej operacji: result_xyz2neu.txt

## Znane błędy
Ze względu na problem z odczytem i wyświetlaniem symbolu stopni '&deg;' wyniki w pliku wyjściowym funkcji `xyz2plh` z opcją `dms` mają postać dd:mm:ss.ss.

W dokumentacji programu niemożliwe jest używanie polskiego znaku 'ś'.
