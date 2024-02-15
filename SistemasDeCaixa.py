from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql


window = Tk()

window.geometry("850x600")
window.title("GERAR FATURAMENTO EM PYTHON")


def quantityFieldListener(a,b,c):
    global quantityVar
    global valorVar
    global itemTaxa
    quantity = quantityVar.get()

    if quantity !="":
        try:
            quantity=float(quantity)
            cost=quantity*itemTaxa
            quantityVar.set("%.2f"%quantity)
            valorVar.set("%.2f"%cost)
        except ValueError:
            quantity=quantity[:-1]
            quantityVar.set(quantity)
    else:
        quantity = 0
        quantityVar.set(quantity)



def costFieldListener(a,b,c):
    global quantityVar
    global valorVar
    global itemTaxa
    valor = valorVar.get()

    if valor !="":
        try:
            valor=float(valor)
            quantity=valor/itemTaxa
            quantityVar.set("%.2f"%quantity)
            valorVar.set("%.2f"%valor)
        except ValueError:
            valor=valor[:-1]
            valorVar.set(valor)
    else:
        valor=0
        valorVar.set(valor)




usernameVar = StringVar()
passwordVar = StringVar()
quantityVar = StringVar()
quantityVar.trace('w',quantityFieldListener)


options=[]
taxaDict = {}

armazenOption=["Gelado","natural"]
itemVariable = StringVar()
#itemVariable.set(options[0])



#######3 variaveis para adicionar itens 
addItemNomeVar = StringVar()
addItemTaxaVar = StringVar()
addItemTipoVar = StringVar()
addItemArmazenamentoVar = StringVar()


####### variaveis de valor

valorVar = StringVar()
valorVar.trace('w',costFieldListener)

billsTV = ttk.Treeview(height=15,columns=('Produto Nome','Quantidade','Valor'))

UpdateTV = ttk.Treeview(height=15,columns=('nome','taxa',"tipo","tipo_armazenamento"))


itemTaxa = 2
taxaVar = StringVar()
taxaVar.set("%.2f"%itemTaxa)

itemLists = list()
totalCost = 0.0
totalCostVar = StringVar()
totalCostVar.set("Valor Total = {}".format(totalCost))

updateItemID = ""

def generate_bill():
    global itemVariable
    global quantityVar
    global itemTaxa
    global valorVar
    global itemLists
    global totalCost
    global totalCostVar

    itemNome = itemVariable.get()
    quantity = quantityVar.get()
    preco = valorVar.get()
    conn = pymysql.connect(host="localhost",user="root",password="",db="cabeloservice")
    cursor = conn.cursor()


    query = "insert into bill (nome,quantidade,taxa,valor)values('{}','{}','{}','{}')".format(itemNome,quantity,itemTaxa,preco)
    cursor.execute(query)
    conn.commit()
    conn.close()



    #dicionario
    listDict = {"nome":itemNome,"taxa":itemTaxa,"quantidade":quantity,"valor":preco}
    itemLists.append(listDict)
    
    totalCost += float(preco)

    quantityVar.set("0")
    valorVar.set("0")

    updateListView()
    totalCostVar.set("Valor Total = {}".format(totalCost))



def onDoubleClick(event):
    global addItemNomeVar
    global addItemTaxaVar
    global addItemTipoVar
    global addItemArmazenamentoVar
    global updateItemID
    item = UpdateTV.selection()
    updateItemID = UpdateTV.item(item,"text")
    item_detail = UpdateTV.item(item,"values")
    item_index = armazenOption.index(item_detail[3])
    addItemTipoVar.set(item_detail[2])
    addItemTaxaVar.set(item_detail[1])
    addItemNomeVar.set(item_detail[0])
    addItemArmazenamentoVar.set(armazenOption[item_index])
    


def updateListView():
    records = billsTV.get_children()
    for element in records:
        billsTV.delete(element)

   

    for row in itemLists :
        billsTV.insert('','end',text=row['nome'],values=(row["taxa"],row["quantidade"],row["valor"]))
   


def getItemLists():
    records = UpdateTV.get_children()
    for elements in records:
        UpdateTV.delete(elements)
    conn = pymysql.connect(host="localhost",user="root",password="",db="cabeloservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = " select * from produtos"
    cursor.execute(query)
    conn.commit()
    data = cursor.fetchall()
    for row in data:
        UpdateTV.insert('','end',text=row['nome_id'],values=(row['nome'],row['taxa'],row['tipo'],row['tipo_armazenamento']))
    UpdateTV.bind("<Double-1>",onDoubleClick)
    conn.close()




def print_bill():
    global itemLists
    global totalCost
    
    print("                                                                     CUPOM ")

    print("CNPJ: 20,123,123/00001-01                                                  ")
    print("R MONJI DAS CRUZES EXEMPLO, 830, ALMIRANTE TAMANDARE                       ")
    print("41995-566  -  PARANA PR                                                    ")
    print("telefone: (41)99999-99999                                                            ")
    print("OPERADOR: GABRIEL                                                          ")
    print("===========================================================================")
    print("                                 PEDIDO                                    ")
    print("===========================================================================")
    print("{:<40}{:<10}{:<15}{:<10}".format("nome","Preço","Quantidade","valor"))

    print("===========================================================================")

    for item in itemLists:
        print("{:<40}{:<10}{:<15}{:<10}".format(item["nome"],item["taxa"],item["quantidade"],item["valor"]))
    print("================================PAGAMENTO==================================")
    print("{:<20}{:<10}{:<15}{:<10}".format("TOTAL DO PEDIDO","","",totalCost))
    print("===========================================================================")
    print("{:<20}{:<10}{:<15}{:<10}".format("TOTAL DO PEDIDO",totalCost,"FORMA DE PAGAMENTO ","DEBITO"))
    print("CPF NÃO INFORMADO                                                          ")
    print("HORA DA COMPRA : 12:30                                                     ")
    print("===========================================================================")
    print("             *** ESTE TICKET NÃO É DOCUMENTO FISCAL ***                    ")
    print("                       OBRIGADO E VOLTE SEMPRE                             ")
    print("===========================================================================")
    print("DISTRIBUIDORA DE BEBIDAS  -  SEUEMAIL@GMAIL.COM")
    





    itemLists = []
    totalCost = 0.0
    updateListView()
    totalCostVar.set("Valor Total = {}".format(totalCost))





def iExit():
    window.destroy()

def moveToUpdate():
    removeAllWidgets()
    updateItemWindow()


def moveToBills():
    removeAllWidgets()
    ViewAllBills()


def readAllData():
    global options
    global taxaDict
    global itemVariable
    global itemTaxa
    global taxaVar

    options=[]
    #taxaDict={}
    conn = pymysql.connect(host="localhost",user="root",password="",db="cabeloservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from produtos"
    cursor.execute(query)
    data = cursor.fetchall()

    count=0
    for row in data:
        count+=1
        options.append(row['nome_id'])
        taxaDict[row['nome_id']]=row['taxa']
        itemVariable.set(options[0])
        itemTaxa = str(taxaDict[options[0]])
    conn.close()
    taxaVar.set(itemTaxa)
    if count ==0:
        removeAllWidgets()
        addItem()
    else:
        removeAllWidgets()  
        mainwindow()




def optionMenuListener(event):
    global itemVariable
    global taxaDict 
    global itemTaxa
    item = itemVariable.get()
    itemTaxa = float(taxaDict[item])
    taxaVar.set("%.2f"%itemTaxa)

    



def removeAllWidgets():
    global window
    for Widget in window.winfo_children():
        Widget.grid_remove()



def updateBillsData():
    records = billsTV.get_children()
    for element in records:
        billsTV.delete(element)

   
    conn = pymysql.connect(host="localhost",user="root",password="",db="cabeloservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * From bill"
    cursor.execute(query)
    data = cursor.fetchall()

        
    for row in data :
        billsTV.insert('','end',text=row['nome'],values=(row["taxa"],row["quantidade"],row["valor"]))

    conn.close()




def adminLogin():
    global usernameVar
    global passwordVar

    username = usernameVar.get()
    password = passwordVar.get()

    conn = pymysql.connect(host="localhost",user="root",password="",db="cabeloservice")
    cursor = conn.cursor()

    query = "select * From usuario where username ='{}' and password = '{}'".format(username,password)
    cursor.execute(query)
    data = cursor.fetchall()
    admin = False
    for row in data:
        admin = True
    conn.close()
    if admin:
       removeAllWidgets()
       addItem()
    else:
        messagebox.showerror("usuario invalido","senha invalida")

def addItemListener():
    removeAllWidgets()
    addItem()




#######################################tela de login#########################################################
def LoginWindow():
    titleLabel = Label(window,text="Faturamento Login",font="Arial 20",fg="black")
    titleLabel.grid(row=0,column=0,columnspan=4,padx=(40,0),pady=(10,0))

    loginLabel = Label(window,text="Administrador Login:",font="arial 8")
    loginLabel.grid(row=1,column=4,padx=20,pady=10)

    usernameLabel = Label(window,text="Usuario:")
    usernameLabel.grid(row=2,column=3)

    passwordLabel = Label(window,text="Senha:")
    passwordLabel.grid(row=3,column=3)

    usernameEntry = Entry(window,textvariable=usernameVar)
    usernameEntry.grid(row=2,column=4)

    passwordEntry = Entry(window,textvariable=passwordVar,show="*")
    passwordEntry.grid(row=3,column=4)

    loginButton = Button(window,text="login",width=10,height=1,command=lambda:adminLogin())
    loginButton.grid(row=4,column=3,columnspan=2)
              

def updateItem():
    global addItemNomeVar
    global addItemTaxaVar
    global addItemTipoVar
    global addItemArmazenamentoVar
    global updateItemID 

    nome  = addItemNomeVar.get()
    taxa  = addItemTaxaVar.get()
    tipo  = addItemTipoVar.get()
    store = addItemArmazenamentoVar.get()

    conn = pymysql.connect(host="localhost",user="root",password="",db="cabeloservice")
    cursor = conn.cursor()

    query = "update produtos set nome='{}', taxa='{}', tipo='{}', tipo_armazenamento='{}' where nome_id='{}'".format(nome,taxa,tipo,store,updateItemID)
    cursor.execute(query)
    conn.commit()
    conn.close()


    addItemNomeVar.set("")
    addItemTaxaVar.set("")
    addItemTipoVar.set("")

    getItemLists()


def addItemFunc():
    global addItemNomeVar
    global addItemTaxaVar
    global addItemTipoVar
    global addItemArmazenamentoVar
    nome  = addItemNomeVar.get()
    taxa  = addItemTaxaVar.get()
    tipo  = addItemTipoVar.get()
    store = addItemArmazenamentoVar.get()
    nomeId = nome.replace(" ","_")

    conn = pymysql.connect(host="localhost",user="root",password="",db="cabeloservice")
    cursor = conn.cursor()

    query = "insert into produtos(nome,nome_id,taxa,tipo,tipo_armazenamento)values('{}','{}','{}','{}','{}')".format(nome,nomeId,taxa,tipo,store)
    cursor.execute(query)
    conn.commit()
    conn.close()
    addItemNomeVar.set("")
    addItemTaxaVar.set("")
    addItemTipoVar.set("")




###########################################Tela PRINCIPAL MENU###########################################################################
def mainwindow():

    removeAllWidgets()

    window.geometry("950x650")
    titleLabel = Label(window,text="Faturamento de Produtos ",font="Arial 30",fg="black")
    titleLabel.grid(row=0,column=1,columnspan=3,pady=(10,0))

    addButton = Button(window,text="Adicionar Produtos",width=15,height=2,bg="orange" ,fg="white",command=lambda:addItemListener())
    addButton.grid(row=1,column=0,padx=(10,0),pady=(10,0))
    
    UpdateNewItem = Button(window,text="Atualizar Produtos",width=15,height=2,bg="orange" ,fg="white",command=lambda:moveToUpdate())
    UpdateNewItem.grid(row=1,column=1,padx=(5,0),pady=(10,0))

    showAllEntry = Button(window,text="Lista de Recibos",width=15,height=2,bg="orange" ,fg="white",command=lambda:moveToBills())
    showAllEntry.grid(row=1,column=2,padx=(5,0),pady=(10,0))

    LogoutBtn = Button(window,text="Sair do Sistema",width=15,height=2,command=lambda:iExit())
    LogoutBtn.grid(row=1,column=4,pady=(10,0))


    itemLabel = Label(window,text="Selecionar Item:")
    itemLabel.grid(row=2,column=0,padx=(5,0),pady=(10,0))

    itemDropDown = OptionMenu(window,itemVariable,*options,command=optionMenuListener)
    itemDropDown.grid(row=2,column=1,padx=(10,0),pady=(10,0))
    ########################################################################

    TaxaLabel = Label(window,text="Preço :")
    TaxaLabel.grid(row=2,column=2,padx=(5,0),pady=(10,0))

    TaxaValor = Label(window,textvariable=taxaVar)
    TaxaValor.grid(row=2,column=3,padx=(5,0),pady=(10,0))

    ########################################################################

    valorLabel = Label(window,text="Valor:")
    valorLabel.grid(row=4,column=2,padx=(10,0),pady=(10,0))

    valorEntry = Entry(window,textvariable=valorVar)
    valorEntry.grid(row=4,column=3,padx=(10,0),pady=(10,0))


    ##########################################################################
    quantityLabel = Label(window,text="Quantidade:")
    quantityLabel.grid(row=3,column=2,padx=(5,0),pady=(10,0))

    quantityEntry = Entry(window,textvariable=quantityVar)
    quantityEntry.grid(row=3,column=3,padx=(5,0),pady=(10,0))


    buttonBill = Button(window,text="Adicionar na lista",command=lambda:generate_bill())
    buttonBill.grid(row=2,column=4,padx=(10,0),pady=(10,0))

    #################################  preview nota fiscal ################################################

    billLabel = Label(window,text="Lista dos Produtos:",font="arial 25")
    billLabel.grid(row=5,column=2)

    billsTV.grid(row=6,column=0,columnspan=5,padx=(20,0))

    ScrollBar=Scrollbar(window,orient="vertical",command=billsTV.yview)
    ScrollBar.grid(row=6,column=4,sticky="NSE")

    billsTV.configure(yscrollcommand=ScrollBar.set)

    billsTV.heading('#0',text="Nome do Produto")
    billsTV.heading('#1',text="Taxa do Produto")
    billsTV.heading('#2',text="Valor do Produto")
    billsTV.heading('#3',text="Quantidade do Produto")



    totalCostLabel = Label(window,textvariable=totalCostVar,bg="orange")
    totalCostLabel.grid(row=8,column=1)


    generateBtnBill = Button(window,text="Gerar Nota Fiscal",command=lambda:print_bill())
    generateBtnBill.grid(row=8,column=4,padx=(10,0),pady=(10,0))



    updateListView()


    








 ############################################### ADICIONAR ITEM #############################  
def addItem():
    removeAllWidgets()
    window.geometry("850x600")


    backButton = Button(window,text="voltar",font="arial 8",command=lambda:readAllData())
    backButton.grid(row=0,column=0,padx=(10,0))

    
    titleLabel = Label(window,text="Adicionar produto",width=40, font="Arial 30",fg="green")
    titleLabel.grid(row=0,column=1,columnspan=5,pady=(10,0))

    ItemNameLabel = Label(window,text="Nome do Produto:",font="arial 8")
    ItemNameLabel.grid(row=1,column=1,pady=(10,0))

    ItemNameEntry = Entry(window,textvariable=addItemNomeVar)
    ItemNameEntry.grid(row=1,column=2)


    ItemTaxaLabel = Label(window,text="Preço do Produto:",font="arial 8")
    ItemTaxaLabel.grid(row=1,column=3,pady=(10,0))

    ItemTaxaEntry = Entry(window,textvariable=addItemTaxaVar)
    ItemTaxaEntry.grid(row=1,column=4)


    ItemTipoLabel = Label(window,text="Tipo do Produto:",font="arial 8")
    ItemTipoLabel.grid(row=2,column=1,pady=(10,0))

    ItemTipoEntry = Entry(window,textvariable=addItemTipoVar)
    ItemTipoEntry.grid(row=2,column=2)


    ItemArmazenamentoLabel = Label(window,text="Tipo Armazenamento do Produto:",font="arial 8")
    ItemArmazenamentoLabel.grid(row=2,column=3,pady=(10,0))

    temArmazenamentoEntry = OptionMenu(window,addItemArmazenamentoVar,*armazenOption)
    temArmazenamentoEntry.grid(row=2,column=4)

    addItembutton = Button(window,text="Adicionar Produto")
    addItembutton = Button(window,text="Adicionar Produto",command=lambda:addItemFunc())
    addItembutton.grid(row=4,column=2,padx=(10,0),pady=(10,0))


def updateItemWindow():
    window.geometry("1050x550")


    backButton = Button(window,text="voltar",font="arial 8",command=lambda:readAllData())
    backButton.grid(row=0,column=0,padx=(10,0))

    
    titleLabel = Label(window,text="Adicionar produto",width=40, font="Arial 30",fg="green")
    titleLabel.grid(row=0,column=1,columnspan=5,pady=(10,0))

    ItemNameLabel = Label(window,text="Nome do Produto:",font="arial 8")
    ItemNameLabel.grid(row=1,column=1,pady=(10,0))

    ItemNameEntry = Entry(window,textvariable=addItemNomeVar)
    ItemNameEntry.grid(row=1,column=2)


    ItemTaxaLabel = Label(window,text="Preço do Produto:",font="arial 8")
    ItemTaxaLabel.grid(row=1,column=3,pady=(10,0))

    ItemTaxaEntry = Entry(window,textvariable=addItemTaxaVar)
    ItemTaxaEntry.grid(row=1,column=4)


    ItemTipoLabel = Label(window,text="Tipo do Produto:",font="arial 8")
    ItemTipoLabel.grid(row=2,column=1,pady=(10,0))

    ItemTipoEntry = Entry(window,textvariable=addItemTipoVar)
    ItemTipoEntry.grid(row=2,column=2)


    ItemArmazenamentoLabel = Label(window,text="Tipo Armazenamento do Produto:",font="arial 8")
    ItemArmazenamentoLabel.grid(row=2,column=3,pady=(10,0))

    temArmazenamentoEntry = OptionMenu(window,addItemArmazenamentoVar,*armazenOption)
    temArmazenamentoEntry.grid(row=2,column=4)

    addItembutton = Button(window,text="Atualizar Produtos")
    addItembutton = Button(window,text="Atualizar Produtos",bg="orange",command=lambda:updateItem())
    addItembutton.grid(row=3,column=3,padx=(10,0),pady=(10,0))

    UpdateTV.grid(row=4,column=0,columnspan=5,padx=(20,0))

    ScrollBar=Scrollbar(window,orient="vertical",command=UpdateTV.yview)
    ScrollBar.grid(row=4,column=4,sticky="NSE")

    UpdateTV.configure(yscrollcommand=ScrollBar.set)

    UpdateTV.heading('#0',text="Código do Produto")
    UpdateTV.heading('#1',text="Nome do Produto")
    UpdateTV.heading('#2',text="Preço")
    UpdateTV.heading('#3',text="Tipo do Produto")
    UpdateTV.heading('#4',text="Tipo de Estoque")

    getItemLists()

def ViewAllBills():
    window.geometry("1050x550")
    backButton = Button(window,text="voltar",font="arial 8",command=lambda:readAllData())
    backButton.grid(row=0,column=0,padx=(10,0))
    titleLabel = Label(window,text="lista de compras",width=40, font="Arial 30",fg="green")
    titleLabel.grid(row=1,column=0,columnspan=5,pady=(10,0))


    billsTV.grid(row=5,column=0,columnspan=5,padx=(20,0))

    ScrollBar=Scrollbar(window,orient="vertical",command=billsTV.yview)
    ScrollBar.grid(row=5,column=4,sticky="NSE")

    billsTV.configure(yscrollcommand=ScrollBar.set)

    billsTV.heading('#0',text="Nome do Produto")
    billsTV.heading('#1',text="Preço do Produto")
    billsTV.heading('#2',text="quantidade do Produto")
    billsTV.heading('#3',text="Valor Total da Venda")

    updateBillsData()

LoginWindow()
window.mainloop()