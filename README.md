# Установка

Перед запуском программы необходимо установить следующие библиотеки:

    pip install requests
    pip install json
 Далее, запустите main.py, передав в качестве аргумента следующие параметры:
 

     python main.py <TOKEN> <SOURCE_ID> <START_DATE> <END_DATE> > result.txt
    
 SOURCE_ID - идентификатор пользователя или сообщества
 START_DATE, END_DATE - начальная и конечная дата в формате YYYYMMDD


Например:

     python main.py <TOKEN> -112510789 20220921 20220921 > result.txt

> Данный скрипт запишет json-объекты публикаций сообщества MASH за 21 сентября 2022 года

## Алгоритм фильтрации по дате
![enter image description here](https://i.ibb.co/61b2d5K/uml.png)
