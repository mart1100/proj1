# Transformacje geodezyjne

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