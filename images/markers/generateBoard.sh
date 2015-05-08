#!/bin/bash

convert black.png marker1.png black.png marker2.png black.png marker3.png black.png marker4.png +append -background none -append row1.png
convert marker5.png black.png marker6.png black.png marker7.png black.png marker8.png black.png +append -background none -append row2.png

convert black.png marker9.png black.png marker10.png black.png marker11.png black.png marker12.png +append -background none -append row3.png
convert marker13.png black.png marker14.png black.png marker15.png black.png marker16.png black.png +append -background none -append row4.png

convert black.png marker17.png black.png marker18.png black.png marker19.png black.png marker20.png +append -background none -append row5.png
convert marker21.png black.png marker22.png black.png marker23.png black.png marker24.png black.png +append -background none -append row6.png

convert black.png marker25.png black.png marker26.png black.png marker27.png black.png marker28.png +append -background none -append row7.png
convert marker29.png black.png marker30.png black.png marker31.png black.png marker32.png black.png +append -background none -append row8.png


convert row1.png +append row2.png  -background none -append   row21.png
convert row3.png +append row4.png  -background none -append   row22.png
convert row5.png +append row6.png  -background none -append   row23.png
convert row7.png +append row8.png  -background none -append   row24.png

convert row21.png +append row22.png  -background none -append   row31.png
convert row23.png +append row24.png  -background none -append   row32.png

convert row31.png +append row32.png  -background none -append   board.png

rm row*.png
