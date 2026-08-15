## Task 1
Напишіть SQL команду, за допомогою якої можна:
вибрати всі стовпчики (За допомогою wildcard “*”) з таблиці products;
вибрати тільки стовпчики name, phone з таблиці shippers,
та перевірте правильність її виконання в MySQL Workbench.

```sql:
select * from products;
select name, phone from shippers;
```

![Result from DB](./img/table.jpg)

![Task 1 result 1](./img/task1-1.jpg)
![Task 1 result 2](./img/task1-2.jpg)

## Task 2

Напишіть SQL команду, за допомогою якої можна знайти середнє, максимальне та мінімальне значення стовпчика price таблички products, та перевірте правильність її виконання в MySQL Workbench*.*

```sql:
select avg(price) as avg, min(price) as min, max(price) as max from products;
```
![Task 2](./img/task2.jpg)


## Task 3

Напишіть SQL команду, за допомогою якої можна обрати унікальні значення колонок category_id та price таблиці products.Оберіть порядок виведення на екран за спаданням значення price та виберіть тільки 10 рядків. Перевірте правильність виконання команди в MySQL Workbench.

```sql:
select distinct category_id, priсe from products order by 2 desc limit 10;
```

-- більш логічний та гарніший варіант:

```sql:
select distinct category_id, sum(price) from products group by 1 order by 2 desc limit 8;
```

![Task 1 option 1](./img/task3.jpg)

![Task 1 option 2](./img/task3-v2.jpg)

## Task 4

Напишіть SQL команду, за допомогою якої можна знайти кількість продуктів (рядків), які знаходиться в цінових межах від 20 до 100, та перевірте правильність її виконання в MySQL Workbench.

```sql:
select count(*) from products where price between 20 and 100 order by price;
```

![Task 4](./img/task4.jpg)

## Task 5

Напишіть SQL команду, за допомогою якої можна знайти кількість продуктів (рядків) та середню ціну (price) у кожного постачальника (supplier_id), та перевірте правильність її виконання в MySQL Workbench.

```sql:
select supplier_id, count(*) as rows_count, avg(price) from products group by supplier_id;
```

![Task 5](./img/task5.jpg)