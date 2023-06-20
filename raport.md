---
papersize: a4
documentclass: article
# geometry: margin=30mm
header-includes:
    - \newcommand{\hideFromPandoc}[1]{#1}
    - \hideFromPandoc{
        \let\Begin\begin
        \let\End\end}
    - \usepackage{graphicx}
    - \setkeys{Gin}{width=.75\textwidth}

...

\Begin{centering}

Techniki Widzenia Maszynowego
--------------

Dąbrowski Paweł
<br>
Dobrowolski Jacek


Mapa wysokości na podstawie ciągu zdjęć
-------------

\End{centering}

Projekt opiera się o metode structure from motion w ramach projektu przebadaliśmy kilka podejść do problemu.

Jako dane wejściowe użyliśmy animacji generowanych za pomocą programu Blender. Obiekty są pokrytę teksturą będącą mieszanką diagramu voronoia oraz szumu. Taka tekstura ma na celu utworzenie elementó które algorytmy mogą śledzić.

![Widok sceny z perspectywą](data/input_perspective.jpg)

![Widok ortogonalny od frontu](data/front.jpg)

### 1. Struktura z gęstego potoku ptycznego.
Pierwsze podejście zostało opartę o gęsty potok optyczny, algorytm Gunnar-Farneback. Metoda estymuje przesunięcie każdego pixela na podstawie szeregu klatek. Metoda może zapewnić lepsze rezultaty jednak ustalenie optymalnych parametró jest nie trywialne. Poniżej zamieszono jedną z klatek wejściowych oraz rezultaty tej metody.

![Dane wejściowe](data/input.png)

![Gęsty Potok Optyczny](data/flow.png)

![Mapa wysokości uzyskana na podstawie potoku optycznego](data/height_map.png)

Jak widać na obrazkach powstaje dużo szumu na płaszczyźnie podłoża.

### 2. SURF

Kolejne podejście zostało opartę o metodę SURF.

![Ogniskowa 35 mm](data/image_focal_35.jpg)

![Ogniskowa 50 mm](data/image_focal_50.jpg)

![Ogniskowa 75 mm](data/image_focal_75.jpg)

