import PySimpleGUI as sg
import psycopg2

sg.theme('DarkBlue')
conn = psycopg2.connect(dbname='coursework', user='postgres', password="postgres", host='localhost')
cursor = conn.cursor()

layoutCheckSales = [[sg.Text('Просмотреть информацию о покупках')], [sg.Button('Просмотр всех покупок')]]
layoutCheckProducts = [[sg.Text('Просмотреть продукты на складе')], [sg.Button('Просмотр продуктов')]]
layoutClientsSale = [[sg.Text('Просмотреть покупки клиента')], [sg.Button('Просмотр покупок клиента')]]
layoutCheckBranch = [[sg.Text('Просмотреть продажи в филиале')], [sg.Button('Посмотреть продажи')]]
layoutCheckClients = [[sg.Text('Просмотреть всех клиентов')], [sg.Button('Просмотр клиентов')]]
layoutPhoneInsert = [[sg.Text('Добавить номер телефона')], [sg.Button('Вставить номер')]]
layoutEmployeeInsert = [[sg.Text('Добавить сотрудника')], [sg.Button('Вставить сотрудника')]]
layoutClientInsert = [[sg.Text('Добавить клиента')], [sg.Button('Вставить клиента')]]
layoutBranchInsert = [[sg.Text('Добавить филиал')], [sg.Button('Вставить филиал')]]
layoutProductInsert = [[sg.Text('Добавить продукт')], [sg.Button('Вставить продукт')]]
layoutSalesInsert = [[sg.Text('Добавить покупку')], [sg.Button('Ввести покупку')]]
layoutUpdate = [[sg.Text('Обновить стоимость продукта')], [sg.Button('Обновить')]]

window = sg.Window('Window Title',
                   (layoutCheckSales, layoutCheckProducts, layoutClientsSale, layoutCheckBranch, layoutCheckClients,
                    layoutPhoneInsert, layoutEmployeeInsert, layoutClientInsert, layoutProductInsert,
                    layoutBranchInsert,
                    layoutSalesInsert, layoutUpdate), size=(500, 720))

numberList = ['рабочий', 'личный']
indlist = [1, 2]

while True:
    cursor.execute("SELECT number from phones")
    comlist_number_2 = cursor.fetchall()
    cursor.execute("SELECT id from phones")
    indlist_number_2 = cursor.fetchall()

    cursor.execute("SELECT name from product")
    comlist_product_2 = cursor.fetchall()
    cursor.execute("SELECT id from product")
    indlist_product_2 = cursor.fetchall()

    cursor.execute("SELECT name from product_type")
    comlist_product_type_2 = cursor.fetchall()
    cursor.execute("SELECT id from product_type")
    indlist_product_type_2 = cursor.fetchall()

    cursor.execute("SELECT country from branchs")
    comlist_branch_2 = cursor.fetchall()
    cursor.execute("SELECT id from branchs")
    indlist_branch_2 = cursor.fetchall()

    cursor.execute("SELECT name from employees_type")
    comlist_employees_type_2 = cursor.fetchall()
    cursor.execute("SELECT id from employees_type")
    indlist_employees_type_2 = cursor.fetchall()

    cursor = conn.cursor()
    cursor.execute("SELECT name from employees")
    comlist_employee_2 = cursor.fetchall()
    cursor.execute("SELECT id from employees")
    indlist_employee_2 = cursor.fetchall()

    cursor.execute("SELECT name from clients")
    comlist_client_2 = cursor.fetchall()
    cursor.execute("SELECT id from clients")
    indlist_client_2 = cursor.fetchall()

    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Вставить номер':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('Номер телефона', size=(15, 1)), sg.InputText()],
            [sg.Text('Тип', size=(15, 1)), sg.Combo(numberList, size=(15, 1))],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '':
                    try:
                        cursor.execute("INSERT INTO phones (number, type) VALUES ( {}, {});".format(
                            "'" + str(valuesEntry[0]) + "'", "'" + str(valuesEntry[1]) + "'"))
                        conn.commit()

                    except (Exception, psycopg2.DatabaseError) as error:
                        print()
                        sg.popup("Выберите тип!", keep_on_top=True)
                        conn.rollback()
                        break
                else:
                    sg.popup("Вы не ввели номер телефона!", keep_on_top=True)
                    break
                conn.commit()

                comlist_number_2.append(valuesEntry[0])
                cursor.execute("select max(id)+1 from phones")
                num = cursor.fetchall()
                indlist_number_2.append(num)
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Вставить сотрудника':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('ФИО', size=(15, 1)), sg.InputText()],
            [sg.Text('Должность', size=(15, 1)), sg.Combo(comlist_employees_type_2, size=(15, 1))],
            [sg.Text('Филиал', size=(15, 1)), sg.Combo(comlist_branch_2, size=(15, 1))],
            [sg.Text('Номер телефона', size=(15, 1)), sg.Combo(comlist_number_2, size=(15, 1))],
            [sg.Text('ID адреса', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '' and str(valuesEntry[1]) != '' and str(valuesEntry[2]) != '' and str(
                        valuesEntry[3]) != '':
                    cursor.execute("INSERT INTO employees (name, idemployees_type, idbranchs, idphones, idadresesses) "
                                   "VALUES ({}, {}, {}, {}, {});".format(
                        "'" + str(valuesEntry[0]) + "'",
                        list(indlist_employees_type_2[comlist_employees_type_2.index(valuesEntry[1])])[0],
                        list(indlist_branch_2[comlist_branch_2.index(valuesEntry[2])])[0],
                        list(indlist_number_2[comlist_number_2.index(valuesEntry[3])])[0], valuesEntry[4]))
                    conn.commit()
                    break
                else:
                    sg.popup("Введите все данные!", keep_on_top=True)
                    break
                conn.commit()
                comlist_employee_2.append(valuesEntry[3])
                cursor.execute("select max(id_employee)+1 from employees")
                num = cursor.fetchall()
                indlist_employee_2.append(num)
                break
            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Вставить клиента':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('ФИО', size=(15, 1)), sg.InputText()],
            [sg.Text('Возраст', size=(15, 1)), sg.InputText()],
            [sg.Text('Номер телефона', size=(15, 1)), sg.Combo(comlist_number_2, size=(15, 1))],
            [sg.Text('ID адреса', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '' and str(valuesEntry[1]) != '' and str(valuesEntry[2]) != '':
                    try:
                        cursor.execute("insert into clients(name, age, idphone, idadresesses) values({}, {}, {}, {}) "
                            .format("'" + str(valuesEntry[0]) + "'", valuesEntry[1],
                            list(indlist_number_2[comlist_number_2.index(valuesEntry[2])])[0], valuesEntry[3]))
                    except (Exception, psycopg2.DatabaseError) as error:
                        print()
                        sg.popup("Age < 18!", keep_on_top=True)
                        conn.rollback()
                        break
                else:
                    sg.popup("Введите все данные!!", keep_on_top=True)
                    break
                conn.commit()
                comlist_client_2.append(valuesEntry[0])
                cursor.execute("select max(id)+1 from clients")
                num = cursor.fetchall()
                indlist_client_2.append(num)
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Вставить филиал':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('Площадь', size=(15, 1)), sg.InputText()],
            [sg.Text('Страна', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '' and str(valuesEntry[1]) != '':
                    cursor.execute("insert into branchs(square, countempl, country) values({}, 0, {}) "
                                   .format(valuesEntry[0], "'" + str(valuesEntry[1]) + "'"))
                else:
                    sg.popup("Введите все данные!", keep_on_top=True)
                    break
                conn.commit()
                comlist_branch_2.append(valuesEntry[1])
                cursor.execute("select max(id)+1 from branchs")
                num = cursor.fetchall()
                indlist_branch_2.append(num)
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Вставить продукт':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('Название', size=(15, 1)), sg.InputText()],
            [sg.Text('Количество', size=(15, 1)), sg.InputText()],
            [sg.Text('Стоимость', size=(15, 1)), sg.InputText()],
            [sg.Text('Вид продукта', size=(15, 1)), sg.Combo(comlist_product_type_2, size=(15, 1))],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '' and str(valuesEntry[1]) != '' and str(valuesEntry[2]) != '' \
                        and str(valuesEntry[3]) != '':
                    cursor.execute("insert into product(name, count, cost, idproduct_type) values({}, {}, {}, {});"
                                   .format("'" + str(valuesEntry[0]) + "'", valuesEntry[1], valuesEntry[2],
                                           list(indlist_product_type_2[comlist_product_type_2.index(valuesEntry[3])])[
                                               0]))
                else:
                    sg.popup("Введите все данные!", keep_on_top=True)
                    break
                conn.commit()
                comlist_product_2.append(valuesEntry[1])
                cursor.execute("select max(id)+1 from product")
                num = cursor.fetchall()
                indlist_product_2.append(num)
                break

            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Просмотр всех покупок':
        query = """SELECT c.name, b.country, p.name, p.cost, sales.count, date FROM sales
join product p on p.id = sales.idproduct
join branchs b on b.id = sales.idbranch
join clients c on c.id = sales.idclient;"""
        cursor.execute(query)
        data = cursor.fetchall()
        my_data = []
        for i in data:
            my_data.append(list(i))
        print(my_data)
        headings = ['client name', 'country', 'product name', 'cost', 'count', 'date']
        layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='left',
                            num_rows=20,
                            alternating_row_color='darkblue',
                            key='-TABLE-',
                            row_height=35)]]

        windowView = sg.Window('The Table Element', layout)

        while True:
            eventView, valuesView = windowView.read()
            print(eventView, valuesView)
            if eventView == sg.WIN_CLOSED:
                break
        windowView.close()

        print("View")

    if event == 'Просмотр продуктов':
        query = """SELECT product.name, count, cost, pt.name FROM product 
join product_type pt on product.idproduct_type = pt.id
where count IS NOT NULL;"""
        cursor.execute(query)
        data = cursor.fetchall()
        my_data = []
        for i in data:
            my_data.append(list(i))
        print(my_data)
        headings = ['name product', 'count', 'cost', 'product type']

        layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='left',
                            num_rows=20,
                            alternating_row_color='darkblue',
                            key='-TABLE-',
                            row_height=35)]]

        windowView = sg.Window('The Table Element', layout)

        while True:
            eventView, valuesView = windowView.read()
            print(eventView, valuesView)
            if eventView == sg.WIN_CLOSED:
                break
        windowView.close()
        print("View")

    if event == 'Просмотр покупок клиента':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('Имя клиента', size=(15, 1)), sg.Combo(comlist_client_2, size=(15, 1))],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if str(valuesEntry[0]) != '':
                if eventEntry == sg.WIN_CLOSED:
                    windowEntry.close()
                    break
                if eventEntry == 'Submit':
                    query = """SELECT clients.name, p.name, pt.name, s.count, s.date from clients
join sales s on clients.id = s.idclient
join clients c on c.id = s.idclient
join product p on p.id = s.idproduct
join product_type pt on pt.id = p.idproduct_type
where clients.id = {};""".format(list(indlist_client_2[comlist_client_2.index(valuesEntry[0])])[0])
                    cursor.execute(query)
                    data = cursor.fetchall()
                    my_data = []
                    for i in data:
                        my_data.append(list(i))
                    print(my_data)
                    headings = ['client name', 'product name', 'product type', 'count', 'date']

                    layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                                        auto_size_columns=True,
                                        display_row_numbers=True,
                                        justification='left',
                                        num_rows=20,
                                        alternating_row_color='darkblue',
                                        key='-TABLE-',
                                        row_height=35)]]
                    if eventEntry == sg.WIN_CLOSED:
                        windowEntry.close()
                        break
                    windowView = sg.Window('The Table Element', layout)
                    while True:
                        eventView, valuesView = windowView.read()
                        print(eventView, valuesView)
                        if eventView == sg.WIN_CLOSED:
                            windowEntry.close()
                            break
                    break
                    print("View")
            else:
                sg.popup("Введите все данные!", keep_on_top=True)
                break

    if event == 'Посмотреть продажи':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('Страна филиала', size=(15, 1)), sg.Combo(comlist_branch_2, size=(15, 1))],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        result = ''
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if str(valuesEntry[0]) != '':
                if eventEntry == sg.WIN_CLOSED:
                    windowEntry.close()
                    break
                if eventEntry == 'Submit':
                    query = """SELECT branchs.id, country, c.name, p.name, s.count
FROM branchs
join sales s on branchs.id = s.idbranch
join clients c on c.id = s.idclient
join product p on p.id = s.idproduct
                where branchs.id = {};""".format(list(indlist_branch_2[comlist_branch_2.index(valuesEntry[0])])[0])
                    cursor.execute(query)
                    data = cursor.fetchall()
                    my_data = []
                    for i in data:
                        my_data.append(list(i))
                    print(my_data)
                    headings = ['branch id', 'country', 'client name', 'product name', 'sale count']

                    layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                                        auto_size_columns=True,
                                        display_row_numbers=True,
                                        justification='left',
                                        num_rows=20,
                                        alternating_row_color='darkblue',
                                        key='-TABLE-',
                                        row_height=35)]]
                    if eventEntry == sg.WIN_CLOSED:
                        windowEntry.close()
                        break
                    windowView = sg.Window('The Table Element', layout)
                    while True:
                        eventView, valuesView = windowView.read()
                        print(eventView, valuesView)
                        if eventView == sg.WIN_CLOSED:
                            windowEntry.close()
                            break
                    break
                    print("View")
            else:
                sg.popup("Введите все данные!", keep_on_top=True)
                break

    if event == 'Просмотр клиентов':
        query = """SELECT name, age FROM clients;"""
        cursor.execute(query)
        data = cursor.fetchall()
        my_data = []
        for i in data:
            my_data.append(list(i))
        print(my_data)
        headings = ['name', 'age']

        layout = [[sg.Table(values=my_data, headings=headings, max_col_width=35,
                            auto_size_columns=True,
                            display_row_numbers=True,
                            justification='left',
                            num_rows=11,
                            alternating_row_color='darkblue',
                            key='-TABLE-',
                            row_height=35)]]

        windowView = sg.Window('The Table Element', layout)

        while True:
            eventView, valuesView = windowView.read()
            print(eventView, valuesView)
            if eventView == sg.WIN_CLOSED:
                break
        windowView.close()
        print("View")

    if event == 'Ввести покупку':
        id_drug = 0
        id_employee = 0
        id_client = ''
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('Имя клиента', size=(15, 1)), sg.Combo(comlist_client_2, size=(15, 1))],
            [sg.Text('Название продукта', size=(15, 1)), sg.Combo(comlist_product_2, size=(15, 1))],
            [sg.Text('Страна филиала', size=(15, 1)), sg.Combo(comlist_branch_2, size=(15, 1))],
            [sg.Text('Количество', size=(15, 1)), sg.InputText()],
            [sg.Text('Дата(гггг-мм-дд)', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '' and str(valuesEntry[1]) != '' and str(valuesEntry[2]) != '' \
                        and str(valuesEntry[3]) != '':
                    if str(valuesEntry[4]) != '':
                        cursor.execute("INSERT INTO sales (idclient, idproduct, idbranch, count, date) "
                                       "VALUES ({}, {}, {},{}, DATE {});".format(
                            list(indlist_client_2[comlist_client_2.index(valuesEntry[0])])[0],
                            list(indlist_product_2[comlist_product_2.index(valuesEntry[1])])[0],
                            list(indlist_branch_2[comlist_branch_2.index(valuesEntry[2])])[0], valuesEntry[3],
                            "'" + str(valuesEntry[4]) + "'"))
                        conn.commit()
                        break
                    else:
                        cursor.execute("INSERT INTO sales (idclient, idproduct, idbranch, count) "
                                       "VALUES ({}, {}, {},{});".format(
                            list(indlist_client_2[comlist_client_2.index(valuesEntry[0])])[0],
                            list(indlist_product_2[comlist_product_2.index(valuesEntry[1])])[0],
                            list(indlist_branch_2[comlist_branch_2.index(valuesEntry[2])])[0], valuesEntry[3]))
                        conn.commit()
                        break
                else:
                    sg.popup("Введите все данные!", keep_on_top=True)
                    break
            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()

    if event == 'Обновить':
        layout = [
            [sg.Text('Пожалуйста, введите необходимые данные.')],
            [sg.Text('Имя продукта', size=(15, 1)), sg.Combo(comlist_product_2, size=(15, 1))],
            [sg.Text('Новая стоимость', size=(15, 1)), sg.InputText()],
            [sg.Submit()]
        ]
        windowEntry = sg.Window('Окно ввода', layout, keep_on_top=True)
        while True:
            eventEntry, valuesEntry = windowEntry.read()
            if eventEntry == 'Submit':
                if str(valuesEntry[0]) != '' and str(valuesEntry[1]) != '':
                    id_product = list(indlist_product_2[comlist_product_2.index(valuesEntry[0])])[0]
                    new_price = valuesEntry[1]
                    cursor.execute("update product set cost = {} " \
                                   "where id = {};".format(new_price, id_product))
                    conn.commit()
                    break
                else:
                    sg.popup("Введите все данные!", keep_on_top=True)
                    break
            if eventEntry == sg.WIN_CLOSED:
                break
        windowEntry.close()
window.close()
conn.close()
