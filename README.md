# Курсач "Научные труды сотрудников"

## При запуске открывается интерфейс с Авторизацией/Регистрацией и сразу много исключений на пароль, модуль auth.py
### Логины уже в бд: Funtik228, 1 ; Пароли уже в бд: Funtik228$, fUNTIK228$ 

## После успешной регистрации или авторизации интерфейс изменяется на таскбар из модуля preloader.py который в flogic папке

### Очень долгий прелоадер специально чтобы показать что что то грузится)))))))

## После прогружения прелоадера открывается интерфейс с таблицей из dlspls.sql которая создается сразу же ( чтобы не вызывать ошибок ) при загрузке этого окна, вот и в этом окне несколько кнопок ( так же если вы скачали отсюда проект то в таблице сразу будут значения которые можно регулировать при нажатии с помощью виджетов )

### Кнопки "Добавить,Поиск,Удалить все" открывают виджеты при нажатии, при нажатии на Добавить можно ввести ФИО и Научный труд, дата регистрации в бд сама сгенерируется ( Ну будет дата с компа взята настоящая ), Поиск кнопка дает возможность поиска по ключевому слову по всей таблице, по поиску ФИО и дате ( Дата красиво с вылетающим скроллом появляется ), кнопка Удалить все удаляет все.

### Есть очень удобная кнопка обновить, которая придумалась путем того, что иногда значения в бд обновлялись не корректно когда изменяешь их в окне, и если такое произошло кликаем ПКМ и появляется кнопка Обновить которая перепроверяет все значения в бд.

# Скриншоты

## Окно авторизации

<img width="497" alt="Снимок экрана 2025-04-16 в 20 10 36" src="https://github.com/user-attachments/assets/c3d34995-1815-4e9c-8ae2-b8afd12ae13a" />

## Окно регистрации

<img width="609" alt="Снимок экрана 2025-04-16 в 20 11 24" src="https://github.com/user-attachments/assets/dce66282-05cd-46d0-9ebf-e14fcabfd5b9" />

## Таскбар

<img width="477" alt="Снимок экрана 2025-04-16 в 20 12 01" src="https://github.com/user-attachments/assets/6f4b6740-6ba7-4cbf-a14b-e787cea30cb6" />
<img width="490" alt="Снимок экрана 2025-04-16 в 20 12 07" src="https://github.com/user-attachments/assets/36c7f26c-2ca8-4e30-b0d0-27a1427456d0" />

## Окно с таблицей


<img width="789" alt="Снимок экрана 2025-04-16 в 20 12 36" src="https://github.com/user-attachments/assets/92bdc225-3085-45a4-82b7-4b4f17be238f" />

### Добавление нового значения через виджет по клику на "Добавить" кнопку

<img width="743" alt="Снимок экрана 2025-04-16 в 20 13 20" src="https://github.com/user-attachments/assets/354b3fc1-cb09-4c53-83dd-8d7947cc87af" />

<img width="791" alt="Снимок экрана 2025-04-16 в 20 14 02" src="https://github.com/user-attachments/assets/e0db9401-a336-472c-adff-010cebfed963" />

### Клик на значение и получаем виджет с новыми кнопками "Удалить" ( Удаление конкретно этой строки ), "Изменить" ( Изменение тоже этой строки которую выбрали )

<img width="761" alt="Снимок экрана 2025-04-16 в 20 15 58" src="https://github.com/user-attachments/assets/7edd18e8-6818-4521-9c31-11a1f1b0254f" />

### Поиск, виджет по клику на "Поиск" кнопку

<img width="765" alt="Снимок экрана 2025-04-16 в 20 14 31" src="https://github.com/user-attachments/assets/82a5afd1-d192-42fd-b154-47bb69e00fe9" />


### Удаляем все по кнопке "Удалить все", после нажатия нас встречает предупреждение

<img width="745" alt="Снимок экрана 2025-04-16 в 20 16 53" src="https://github.com/user-attachments/assets/25571b61-a575-4683-bd2b-3bce6db19515" />






 



