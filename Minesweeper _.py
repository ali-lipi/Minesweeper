#создаём игровое поле
#исп-ем tkinter, а не pygame
#1. создаем поле, с меню и контурами

import tkinter as tk

from random import shuffle #ф-я из модуля random позволяет перемешивать коллекцию

from tkinter.messagebox import showinfo, showerror
#доп.модуль с разным типом сообщений (окончание игры)
#showinfo позволяет создать диалоговое окно

colours = {
    0: 'white',
    1: '#32a8a2',
    2: '#32a852',
    3: '#752332',
    4: '#914d19',
    5: '#5032a8',
    6: '#91196f',
    7: 'ff9412',
    8: '#ff1a12',
}

#класс для переименовывания ткинтеровской кнопки, переопределяю метод
#название ткинтеровской кнопки неиформативное

class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwarg):
    #master - окно, в котором создается кнопка
    #x - строка, y - столбец
    #**kwarg - принимаем все аргументы (например, width, font)
    #вызвать метод init у самой кнопки button, чтобы сначала создалась "старая" кнопка
        super(MyButton, self).__init__(master, *args, **kwarg)
        self.x = x #это атрибуты для каждой кнопки
        self.y = y
        self.number = number #у каждой кнопки свой номер
        self.is_mine = False #по умолчанию - все кнопки без мин
        self.count_bomb = 0 #счетчик бомб для клеток-соседей
        self.is_open = False #атрибут проверки, открывали мы кнопку или нет
    
    def __repr__(self):
        return f'MyButton{self.x} {self.y} {self.number} {self.is_mine}' #вывод имени с координатами

class MineSweeper: #перечисляем атрибуты
    
    window = tk.Tk()
    #2. "рисуем" игровое поле. row и column не должны меняться
    #т.е. они константы. поле похоже на таблицу
    #а таблицы в питоне проще и удобнее хранить в двухмерных списках
    #3.создаем список кнопок
    row = 10 #указываем количетсво рядов/строк
    column = 7 #указываем кол-во колонок/столбцов
    MINES = 10 #кол-во мин
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True #отвечает за первый клик, исключаем бомбу при первом клике в игре


    def __init__(self): #запуск автоматически
        self.buttons = []#пустой список, куда мы должны "сложить" кнопки
        #убрала из-за барьерных кнопок. count = 1 #для нумерации кнопок и расстановки бомб
        #обходим все ячейки(строки и столбцы и создаем кнопки игрового поля)
        for i in range(MineSweeper.row + 2): #2 доп.ряды и столбцы
            temp = [] #временный список
            for j in range(MineSweeper.column + 2):
                #обращаемся к классу Button и указываем, что он созд-ся в нашем окне
                btn = MyButton(MineSweeper.window, x = i, y = j, width = 3, font='Calibri 15 bold')
                #поэтому window создаем до этого цикла
                #width - ширина ячеек, font-шрифт, calibri 15 - тип и размер шрифта, bold - жирный шрифт
                btn.config(command=lambda button=btn: self.click(button)) #после создания кнопки вызывает метод config
                btn.bind("<Button-3>", self.right_click)
                #анонимная ф-я должна вызвать клик и передать переменную (button)
                #здесь анонимная ф-я lambda служит проводником для корректного создания кнопки
                temp.append(btn) #здесь накопится 7 кнопок
            #после сбора семи кнопок добавляем ряд в список buttons
            self.buttons.append(temp)


    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        current_button = event.widget
        if current_button['state'] == 'normal':
            current_button['state'] = 'disabled'
            current_button['text'] = '✓'
            current_button['disabledforeground'] = 'red' #цвет галочки
        elif current_button['text'] == '✓':
            current_button['text'] = ''
            current_button['state'] = 'normal'
 #напоминалка. обращаемся через класс. к экземпляру обращаемся через self
   
    def click(self, clicked_button: MyButton): #что происходит при клике на кнопку
       
        if MineSweeper.IS_GAME_OVER: #блокируем нажатие кнопок поля после завершения игры
            return None #можно просто return, без значения None


        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number) #передаем значение number функции insert_mines
            self.count_mines_in_buttons()
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False #чтобы поле не переформировывалось бесконечно (а только после первого клика)

        if clicked_button.is_mine:
            clicked_button.config(text = '*', background = 'red', disabledforeground = 'black')
            #background - фон кнопки-бомбы, disabledforeground - цвет текста
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game Over', 'Вы проиграли!') #в случае проигрыша
        
            for i in range(1, MineSweeper.row + 1):
                        for j in range(1, MineSweeper.column + 1):
                            btn = self.buttons[i][j]
                            if btn.is_mine:
                                btn['text'] = '*' #после нажатия ОК в окне появятся все бомбы

        else:
            colour = colours.get(clicked_button.count_bomb, 'black') #black - условие для цифр, которых нет в словаре
            
            if clicked_button.count_bomb: #цвет цифр
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground = colour)
                clicked_button.is_open = True
                
            else:
                #clicked_button.config(text='', disabledforeground = colour) #если 0 бомб рядом, то пустая кнопка, закомментила, испол-ю метод поиск в ширину
                self.breadth_first_search(clicked_button)
            clicked_button.config(state='disabled') #исключаем повторное нажатие на кнопку
            clicked_button.config(relief=tk.SUNKEN) #видно, что кнопка нажималась

    #если в кнопке нужно вывести номер кнопки (индикатор), а не кол-во бомб - clicked_button.number
    #:MyButton - хинт среде, что будем работать с объектами кнопок
    # #передать инфу о клетке (бомба или кол-во из вокруг)
        #передать инфу по кнопке, которая была нажата
        #print(clicked_button)
       

    def breadth_first_search(self, btn: MyButton):

        queue = [btn] #список - наша очередь (реализация алгоритма обхода в ширину)
        #добавила одну кнопку и от нее начинаю обходить её соседей
        while queue: #пока есть кнопки в очереди

            cur_btn = queue.pop() #переменная - текущая кнопка
            colour = colours.get(cur_btn.count_bomb, 'black') #black - условие для цифр, которых нет в словаре
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground = colour)
            else:
                cur_btn.config(text='', disabledforeground = colour)
            cur_btn.is_open = True
            cur_btn.config(state='disabled') #делаем кнопку неактивной, исключаем повторное нажатие на кнопку
            cur_btn.config(relief=tk.SUNKEN) #видно, что кнопка нажималась

            #теперь смотрим на 'соседей' кнопки, которая не имеет бомб
            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        #if not abs(dx - dy) == 1: эта часть не давала открыть соседей наискосок
                            #print(x + dx, y + dy) - для проверки условия if abs(dx - dy) == 1:
                            #continue
                
                        next_btn = self.buttons[x + dx][y + dy] #следующая, соседняя кнопка
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.row and \
                            1 <= next_btn.y <= MineSweeper.column and next_btn not in queue:
                            #если кнопка не была открыта и не барьерная
                            queue.append(next_btn)                    

    
    def reload(self): #перезапуск игры (Меню-Играть)
        #удаляю все элементы старой игры и создаю новые
        #self.window.winfo_children()[0].destroy() 
        # #описание шага в конспекте
        [child.destroy() for child in self.window.winfo_children()]
        #наполняем новыми кнопками
        self.__init__() #создание кнопок
        self.create_widgets() #отрисовка кнопок
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False

    def create_settings_window(self):
        window_settings = tk.Toplevel(self.window)
        window_settings.wm_title('Настройки') #добавление заголовка в настройках
        tk.Label(window_settings, text='Количество строк:').grid(row=0, column=0)
        row_entry = tk.Entry(window_settings)
        row_entry.insert(0, MineSweeper.row)
        row_entry.grid(row=0, column=1, padx=20, pady=20) #padx, pady - отступы по x и y
        tk.Label(window_settings, text='Количество столбцов:').grid(row=1, column=0)
        column_entry = tk.Entry(window_settings)
        column_entry.insert(0, MineSweeper.column)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(window_settings, text='Количество мин:').grid(row=2, column=0)
        mines_entry = tk.Entry(window_settings)
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        #создание кнопки для сохранения настроек
        save_settings_btn = tk.Button(window_settings, text='Применить', command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        save_settings_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20) #columnspan - атрибут, объединение двух колонок
        #здесь padx, pady добавляют отступ от края поля(расстояние между кнопкой и краем поля)
    
    # функция change_settings должна получать доступ к полям ввода в настройках
    
    def change_settings(self, row: tk.Entry, column: tk.Entry, MINES: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(MINES.get())
        except ValueError:
            showerror('Ошибка','Вы ввели некорректное значение!')
            return

        MineSweeper.row = int(row.get()) #обязатально int, иначе примет строку
        MineSweeper.column = int(column.get())
        MineSweeper.MINES = int(MINES.get())
        self.reload() #перезапуск игры - обновление игрового поля

    def create_widgets(self):

        menubar = tk.Menu(self.window) #создание выпадающего меня иприкрепление к окну
        self.window.config(menu = menubar) #располажение на окне, вызов config
        
        settings_menu = tk.Menu(menubar, tearoff=0) #создание подменю
        #tearoff - пунктирная меню надо выпадающим меню, 0 = удаление данной линии
        #добавление лэйблов верхних кнопок
        settings_menu.add_command(label='Играть', command = self.reload) #перезапуск игры
        settings_menu.add_command(label='Настройки', command=self.create_settings_window)
        settings_menu.add_command(label='Выход', command = self.window.destroy) #destroy вызовется автоматически по клику
        menubar.add_cascade(label ='Файл', menu = settings_menu) #объединение в один каскад

        count = 1
        #отображение интерфейса. кнопки лучше всего размещать при помощи метода grid        
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.column + 1):

        #for i in range(MineSweeper.row + 2): #была прорисовка барьерных кнопок, скрыла их
            #for j in range(MineSweeper.column + 2):
                #+2 -метод барьерных элементов, у всех кнопок по 8 соседей
                #достаем кнопку из нашего списка
                btn = self.buttons[i][j] #создаём кнопку
                btn.number = count #назначаем ей номер
                btn.grid(row = i, column = j, stick = 'NWES')
                #stick - позволяет растянуть кнопки по отношению к сторонам света (чтобы не было зазоров при расятгивании окна)
                #NWES - перечислена каждая из сторон света
                count += 1

                #фиксируем игровую область (строки и столбцы для команды "развернуть")
            for i in range(1, MineSweeper.row + 1):
                 MineSweeper.window.rowconfigure(i, weight=1)
            for j in range(1, MineSweeper.column + 1):
                MineSweeper.window.columnconfigure(j, weight=1)

    def open_all_buttons(self): #цвет
        
        for i in range(MineSweeper.row + 2):
            for j in range(MineSweeper.column + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*', background='red', disabledforeground='black')
                elif btn.count_bomb in colours: #цвет цифр у соседей
                    colours.get(btn.count_bomb, 'black') #black - условие для цифр, которых нет в словаре
                    btn.config(text=btn.count_bomb, disabledforeground='black')

    def start(self):
        
        self.create_widgets() #пример инкапсуляции
        #self.insert_mines() - перенос в ф-ю click
        #self.count_mines_in_buttons() - перенос в ф-ю click
        #self.print_buttons() - перенос в ф-ю click
        #self.open_all_buttons() #скрыла, чтобы при запуске не было видно итоговой раскладки игрового поля/миин
        MineSweeper.window.mainloop() #вызов нарисованного игрового поля

    def print_buttons(self):
        #for row_btn in self.buttons: #вывод кнопок
            #print(row_btn) #выводилась инфа о кнопке
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.column + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end = '')
                else:
                    print(btn.count_bomb, end = '')
            print()

    def insert_mines(self, number: int): #расстановка мин #number - принимаем number
        index_mines = self.get_mines_places(number)
        print(index_mines)
        #count = 1 перенесла в create_widgets
        for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.column + 1):
                btn = self.buttons[i][j]
                #btn.number = count - в create_widgets, устраняем вариант бомбы на первом клике
                if btn.number in index_mines:
                    btn.is_mine = True
                #count += 1 - перенос в create_widgets
                
    def count_mines_in_buttons(self):
         for i in range(1, MineSweeper.row + 1):
            for j in range(1, MineSweeper.column + 1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0 , 1]: #получим все варианты соседей клетки
                        for col_dx in [-1, 0 , 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                count_bomb += 1
                btn.count_bomb = count_bomb
                

    @staticmethod #ниже не используем self в def

    def get_mines_places(exclude_number: int): #расстановка мин. возвращаю индексы мин
        #exclude_number - номер, который должны исключить (первая кнопка/клик не должна быть боибой)
        indexes = list(range(1, MineSweeper.column * MineSweeper.row + 1))
        indexes.remove(exclude_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]


game = MineSweeper() #для инициализации игры, до вызова должна все прописать
game.start()
