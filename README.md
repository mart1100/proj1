# Transformacje geodezyjne

## Spis treści 
* [Ogólne informacje](#ogólne-informacje)
* [Wymagania sprzętowe](#wymagania-sprzętowe)
* [Funkcje](#funkcje)
* [Uruchomienie programu](#uruchomienie-programu)
* [Przykłady użycia](#przykłady-użycia)
* [Znane błędy](#znane-błędy)

## Ogólne informacje
Celem programu jest transformacja współrzędnych geocentrycznych ECEF stacji permanentnej GNSS w Józefosławiu z pliku (X,Y,Z), między danymi układami współrzędnych geodezyjnych i ortokartezjańskich. Ten program umożliwia przeliczenie: współrzędnych ortokartezjaśkich na współrzedne geodezyjne, współrzędnych geodezyjnych (fi, lambda, h) na ortokartezjańskie, współrzędnych geodezyjnych do układów odniesienia na terenie Polski (PL2000, PL1992). Program obsługuje elipsoidy WGS84, GRS80, i elipsoidę Krasowskiego.
Projekt powstał w celu utrwalenia informacji zdobytych na zajęciach z Informatyki Geodezyjnej.

## Wymagania sprzętowe
Wymagania, które musi spełnić komputer użytkownika:
1. Posiadanie wersji programu Python 3.0 lub wyższej.
2. Zainstalowane biblioteki sys oraz math
3. Dane wejściowe muszą być zapisane w pliku tekstowym.
4. Posiadanie systemu operacyjnego Windows, MacOS lub Linux.

## Funkcje:
Lista funkcji, które 
--xyz2plh: Wykorzystując algorytm Hirvonena, przelicza współrzędne ortokartezjańskie (x, y, z) na współrzędne geodezyjne (phi, lambda, h).
--plh2xyz: Przelicza współrzędne geodezyjne (phi, lambda, h) na współrzędne ortokartezjańskie (x, y, z).
--pl21992: Przelicza współrzędne geodezyjne (phi, lambda) do układu 1992.
--pl22000: Przelicza współrzędne geodezyjne (phi, lambda) do układu 2000.
--deg2dms: Zamienia stopnie dziesiętna na stopnie, minuty i sekundy.

## Uruchomienie programu
Program należy uruchomić za pomocą Terminala lub Microsoft PowerShell, wpisując w wiersz poleceń komendę:
python skrypt.py [--funkcja] wsp_inp.txt

gdzie w miejscu flagi [--funkcja] należy wpisać jedną z interesujących nas funkcji programu, a plik tekstowy wsp_inp.txt zawiera nasze współrzędne.

## Przykłady użycia
1. Przeliczanie współrzędnych ortokartezjańskich na współrzędne geodezyjne.
Parametrami wejściowymi są:
X, Y, Z : FLOAT,współrzędne w układzie orto-kartezjańskim, 
Parametrami wyjściowymi są:

W wierszu poleceń należy wpisać komendę:
python skrypt.py [--xyz2plh] wsp_inp.txt

W ten sposób powstaje plik tekstowy zawierający wyniki tej operacji: result_xyz2plh.txt

2. Przeliczenie współrzędnych geodezyjnych do układu PL1992.
Parametrami wejściowymi są:
*phi: FLOAT, [stopnie dziesiętne] - szerokosć geodezyjna
*lam: FLOAT, [stopnie dziesiętne] - długosć geodezyjna
Parametrami wyjściowymi są:
*x1992 : FLOAT, [m] - odcięta w układzie 1992
*y1992 : FLOAT, [m] - rzędna w układzie 1992

W wierszu poleceń należy wpisać komendę:
python skrypt.py [--pl21992] wsp_inp.txt

W ten sposób powstaje plik tekstowy zawierający wyniki tej operacji: result_pl21992.txt

## Znane błędy
W dokumentacji programu niemożliwe jest używanie polskiego znaku 'ś'.