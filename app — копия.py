from tkinter import *
from tkinter import ttk
import ctypes
from tkinter.messagebox import showinfo,showerror
import PythonDLL

def defineMethods():
    # region ОПРЕДЕЛЕНИЕ ФУНКЦИЙ
    Library.Insert.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    Library.Insert.restype = ctypes.c_int

    Library.Remove.argtypes = [ctypes.c_int, ctypes.c_int]
    Library.Remove.restype = ctypes.c_int

    Library.Clear.argtypes = []
    Library.Clear.restype = None

    Library.GetLength.argtypes = []
    Library.GetLength.restype = ctypes.c_int

    Library.FindByInf.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    Library.FindByInf.restype = ctypes.POINTER(ctypes.c_int)

    Library.FindByChar.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    Library.FindByChar.restype = ctypes.POINTER(ctypes.c_int)

    Library.FreeArray.argtypes = [ctypes.POINTER(ctypes.c_int)]
    Library.FreeArray.restype = None

    Library.GetInf.argtypes = [ctypes.c_int]
    Library.GetInf.restype = ctypes.c_int

    Library.GetChar.argtypes = [ctypes.c_int]
    Library.GetChar.restype = ctypes.c_int

    Library.GetPrev.argtypes = [ctypes.c_int]
    Library.GetPrev.restype = ctypes.c_int

    Library.GetNext.argtypes = [ctypes.c_int]
    Library.GetNext.restype = ctypes.c_int

    # endregion

libPascal=ctypes.CDLL("./PascalDLL.dll")
libCpp=ctypes.CDLL("./C++DLL.dll")
libC=ctypes.CDLL("./cDLL.dll")
pythonList=PythonDLL.List()
Library=libC  # по умолчанию C
defineMethods()
loaded_libraries={libPascal,libCpp,libC,pythonList}
LibIsPython=False


def cleanup():
    for lib in loaded_libraries:
        lib.Clear()
        print(f"Библиотека: {lib} очищена")

def on_closing():
    cleanup()
    root.destroy()

#ОБРАБОТКА ВЫБОРА ДЕЙСТВИЯ (ДОБАВИТЬ/УДАЛИТЬ)
def comboBoxPL_selected(event):
    global Library, LibIsPython, pythonList
    LibIsPython=False
    language=comboBoxPL.get()
    if language == "Pascal":
        Library = libPascal
    elif language == "C++":
        Library = libCpp
    elif language == "C":
        Library = libC
    elif language=="Python":
        '''if pythonList is None:
            import PythonDLL
            pythonList=PythonDLL.List()'''
        LibIsPython=True
        Library=pythonList
    if not LibIsPython:
        #loaded_libraries.add(Library)
        defineMethods()
    Update()

def item_selected(event):
    selected=table.selection()
    if selected:
        entryIndex.delete(0,END)
        entryIndex.insert(0,str(table.item(selected[0],'values')[0]))

def comboBoxAction_select(event):
    groups={
        "groupIndex":groupIndex,
        "groupInf":groupInf,
        "groupChar":groupChar,
        "buttonAction":buttonAction #pady=(5,0)
    }
    for group in groups.values():
        group.pack_forget()

    selected=comboBoxAction.get()
    if "Удалить" in selected:
        groupIndex.pack(fill="x")
        buttonAction.pack(fill="x",pady=(5,0))
    elif selected=="Добавить новый элемент":
        groupInf.pack(fill="x")
        groupChar.pack(fill="x")
        buttonAction.pack(fill="x",pady=(5,0))
    else:
        groupIndex.pack(fill="x")
        groupInf.pack(fill="x")
        groupChar.pack(fill="x")
        buttonAction.pack(fill="x", pady=(5, 0))

def ClearList():
    for tlib in loaded_libraries:
        #Library.Clear()
        tlib.Clear()
    showinfo("","Список очищен")
    Update()

def GetLength():
    showinfo(title="Длина списка",message=f"Длина списка: {Library.GetLength()}")

def Update():
    for row in table.get_children():
        table.delete(row)
    n = Library.GetLength()
    for i in range(n):
        inf = Library.GetInf(i)
        ch_code = Library.GetChar(i)
        if ch_code:
            ch = chr(ch_code)
        else:
            ch=""
        next=Library.GetNext(i)
        prev=Library.GetPrev(i)
        table.insert("",END,values=(i+1,inf,ch,prev+1,next+1))

def Execute():
    res=0
    if "Добавить" in comboBoxAction.get():
        try:
            inf=int(entryInf.get())
        except:
            showerror("Ошибка", "Введите целое число")
            return
        ch_str=entryChar.get()
        if not(ch_str):
            showerror("Ошибка", "Введите символ")
            return
        if ch_str:
            ch = ord(ch_str[0])
            if not('a' <= entryChar.get()[0] <= 'z' or 'A' <= entryChar.get()[0] <= 'Z'):
                showerror("Ошибка", "Только латинский алфавит")
                return
        for tlib in loaded_libraries:
            if comboBoxAction.get()=="Добавить новый элемент":
                #res=Library.Insert(0, 0, inf, ch)
                res = tlib.Insert(0, 0, inf, ch)
            if comboBoxAction.get()=="Добавить элемент перед i-м":
                #res=Library.Insert(-1,int(entryIndex.get()),inf,ch)
                res = tlib.Insert(-1, int(entryIndex.get()), inf, ch)
            if comboBoxAction.get()=="Добавить элемент после i-го":
                #res=Library.Insert(1,int(entryIndex.get()),inf,ch)
                res = tlib.Insert(1, int(entryIndex.get()), inf, ch)
        entryInf.delete(0,END)
        entryChar.delete(0,END)
    if "Удалить" in comboBoxAction.get():
        for tlib in loaded_libraries:
            if not entryIndex.get():
                return
            if comboBoxAction.get()=="Удалить i-й элемент":
                #res=Library.Remove(0,int(entryIndex.get()))
                res = tlib.Remove(0, int(entryIndex.get()))
            if "перед" in comboBoxAction.get():
                #res=Library.Remove(-1, int(entryIndex.get()))
                res = tlib.Remove(-1, int(entryIndex.get()))
            if "после" in comboBoxAction.get():
                #res=Library.Remove(1, int(entryIndex.get()))
                res = tlib.Remove(1, int(entryIndex.get()))
        entryIndex.delete(0,END)
    if res!=0:
        showerror("Ошибка", "Не удалось выполнить операцию")
    Update()

def Find():
    indices=[]
    count=ctypes.c_int()
    ptr=None

    if mode.get()==1:
        try:
            inf=int(entryFind.get())
        except:
            showerror("Ошибка", "Введите целое число")
            return
        if not LibIsPython:
            ptr=Library.FindByInf(inf,ctypes.byref(count))
        else:
            indices=Library.FindByInf(inf)
    if mode.get()==2:
        ch=entryFind.get()
        if not(ch):
            showerror("Ошибка", "Введите символ")
            return
        if not LibIsPython:
            ptr = Library.FindByChar(ord(ch[0]), ctypes.byref(count))
        else:
            indices=Library.FindByChar(ch[0])

    ucount=len(indices) if LibIsPython else count.value

    if ucount==0:
        showinfo("Поиск элементов", "Элементы не найдены")
        return
    if not LibIsPython and not ptr:
        showerror("Ошибка", "Ошибка при поиске (ptr is null)")
        return

    try:
        if not LibIsPython:
            indices = [ptr[i] for i in range(ucount)]
        showinfo("Результат поиска",f"Найдено элементов: {ucount}\n"f"Индексы: {', '.join(map(str, indices))}")
    finally:
        Library.FreeArray(0 if LibIsPython else ptr)

#region ИНТЕРФЕЙС
root=Tk()
root.title("Циклический двусвязный список (DLL)")
root.geometry("800x450")

#ВЫБОР ЯЗЫКА ПРОГРАММИРОВАНИЯ ДЛЯ ПОДКЛЮЧЕНИЯ ДИНАМИЧЕСКОЙ БИБЛИОТЕКИ
frameLeft=Frame()
framePL=Frame(frameLeft)
framePL.pack(anchor="center")
PL=["C","C++","Pascal","Python"]
labelPL=Label(framePL,text="Выбор ЯП для DLL")
labelPL.pack(fill="x")
comboBoxPL=ttk.Combobox(framePL,values=PL,width=25,state="readonly")
comboBoxPL.current(0)
comboBoxPL.pack(fill="x")
comboBoxPL.bind('<<ComboboxSelected>>', comboBoxPL_selected)

#frameLeft - ТАБЛИЦА ДЛЯ ЦИКЛИЧЕСКОГО ДВУСВЯЗНОГО СПИСКА

frameLeft.pack(side=LEFT,fill="both",expand=True)

frameCP=Frame(frameLeft) #CP - Command Panel
frameCP.pack(fill="x",pady=(5,10))
labelTable=Label(frameCP,text="Текущий список")
labelTable.pack(side=LEFT,expand=True, anchor="center")
buttonUpdate=Button(frameCP,text="Обновить список",command=Update)
buttonUpdate.pack(side=RIGHT,padx=17)

frameTable=Frame(frameLeft)
frameTable.pack(fill="both",expand=True)
scrollbar=ttk.Scrollbar(frameTable)
scrollbar.pack(side=RIGHT,fill="y")

columns=("index","number","char","last_prev","next_prev")
table=ttk.Treeview(frameTable,columns=columns,show="headings",yscrollcommand=scrollbar.set,height=15)
table.heading("index",text="Индекс")
table.heading("number",text="Число")
table.heading("char",text="Символ")
table.heading("last_prev",text="Номер предыдущего")
table.heading("next_prev",text="Номер следующего")
table.column("index", width=50, anchor="w")
table.column("number", width=100, anchor="w")
table.column("char", width=100, anchor="w")
table.column("last_prev", width=150, anchor="w")
table.column("next_prev", width=150, anchor="w")
table.pack(side=LEFT, expand=True,fill="both")
table.bind("<<TreeviewSelect>>",item_selected)
scrollbar.config(command=table.yview)

#frameRight - ФРЕЙМЫ ДЛЯ ДЕЙСТВИЙ СО СПИСКОМ
frameRight=Frame()
frameRight.pack(side=LEFT,fill="y",padx=5,pady=5)

frameAct=Frame(frameRight,borderwidth=3,relief="groove",padx=5,pady=5)
frameAct.pack(fill="x",pady=5)
buttonClear=Button(frameAct,text="Очистить список",command=ClearList)# ВЫВЕСТИ УВЕДОМЛЕНИЕ ПОЛЬЗОВАТЕЛЕЮ (MESSAGE BOX)
buttonClear.pack(fill="x",pady=(0,5))
buttonLength=Button(frameAct,text="Определить длину списка",command=GetLength)
buttonLength.pack(fill="x")

frameChange=Frame(frameRight,borderwidth=3,relief="groove",padx=5,pady=5)
frameChange.pack(fill="x",pady=5)
labelChange=Label(frameChange,text="Изменение структуры")
labelChange.pack(fill="x")
actions=["Добавить новый элемент", "Добавить элемент перед i-м", "Добавить элемент после i-го",
         "Удалить i-й элемент", "Удалить элемент перед i-м", "Удалить элемент после i-го"]
comboBoxAction=ttk.Combobox(frameChange,values=actions,width=27,state="readonly")
comboBoxAction.current(0)
comboBoxAction.pack(fill="x")
comboBoxAction.bind('<<ComboboxSelected>>', comboBoxAction_select)

groupIndex=Frame(frameChange)
labelIndex=Label(groupIndex,text="Индекс")
labelIndex.pack(anchor="w")
entryIndex=Entry(groupIndex)
entryIndex.pack(fill="x")
#groupIndex.pack(fill="x")

groupInf=Frame(frameChange)
labelInf=Label(groupInf,text="Число")
labelInf.pack(anchor="w")
entryInf=Entry(groupInf)
entryInf.pack(fill="x")
groupInf.pack(fill="x")

groupChar=Frame(frameChange)
labelChar=Label(groupChar,text="Символ")
labelChar.pack(anchor="w")
entryChar=Entry(groupChar)
entryChar.pack(fill="x")
groupChar.pack(fill="x")

buttonAction=Button(frameChange,text="Выполнить",command=Execute)
buttonAction.pack(fill="x",pady=(5,0))

#frameFind ПОИСК ЗНАЧЕНИЙ В СПИСКЕ
frameFind=Frame(frameRight,borderwidth=3,relief="groove",padx=5,pady=5)
frameFind.pack(fill="x",pady=5)

labelFind=Label(frameFind,text="Поиск")
labelFind.pack()

mode = IntVar()
mode.set(1)
Radiobutton(frameFind, text="по числу", variable=mode, value=1).pack(anchor="w")
Radiobutton(frameFind, text="по символу", variable=mode, value=2).pack(anchor="w")

entryFind=Entry(frameFind)
entryFind.pack(fill="x")

buttonFind=Button(frameFind,text="Найти",command=Find)
buttonFind.pack(fill="x",pady=(5,0))

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
#endregion ИНТЕРФЕЙС