# Coordinates_Astra
  Этот проект создавался во время моей работы геофизиком.
  Работа заключалась в прохождении сети профилей (ПР/PR) и измерении электрического поля на пикетах (ПК/PK), проектные координаты которых нам выдавал заказчик.
Для ориентации на местности нами использовались GPS-навигаторы Garmin, средняя погрешность которых составляет круг радиусом 3 метра.
Для повышения точности интерпретации данных на каждом измеренном ПК в навигатор записывались координаты измерения.

  Проблема заключалась в том, что запись имени точки в навигатор в формате "ПР-ПК" не представлялось возможным в виду затрачиваемого времени на ручной ввод и человеческого фактора.
Для решения этой проблемы было решено написать скрипт, соотносящий данные из базы координат, предоставленных заказчиком и базы координат, выгруженных с навигаторов.

  Данные со всех навигаторов были собраны в один файл, приведены в одну систему координат с данными заказчика и отсортированы по долготе и широте.
Затем при сравнении двух баз,  фактическим координатам  присваивались ПР и ПК из базы проектных координат, если они находились на расстоянии меньше 8 метров друг от друга.
8 метров было выбрано как предельное расстояние, на котором измерение поля считалось валидным, и т.к. расстояние между пикетами составляло 50 метров, исключалась возможность присвоения ложных ПР,ПК с близлежащих точек измерения

  Основной задачей было нахождение соответствующих пар ПР,ПК для фактических координат, также дополнительно было подсчитано количество пропущенных нами точек, среднее отклонение от 
проектных координат, для первичной оценки измеренных данных были построены псевдокарты распределения каж. удельного сопротивления и заряжаемости.

  Этот проект будет дополняться по мере выполнения электроразведочных работ.

Работы разбиты на три участка и результаты по каждой из них можно посмтреть отдельно
All_stages- визуализация результатов со всех участков работ.
Stage1 - визуализация 1 участка
Stage2 - визуализация 2 участка
Stage3 - визуализация 3 участка, результаты измерений на этом участке на данный момент отсутствуют.

Использованные библиотеки:
Numpy, Pandas, Matplotlib, Os

 
  
