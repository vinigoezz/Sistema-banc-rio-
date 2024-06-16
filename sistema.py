from tkinter import *
import os

master = Tk()
master.title("Sistema Bancário")

fonte_padrao = ("Calbri",12)

def terminar_reg():

    nome = nome_temp.get()
    idade = idade_temp.get()
    cpf = cpf_temp.get()
    senha = senha_temp.get()
    todas_contas = os.listdir()
    
    if nome == "" or idade == "" or cpf == "" or senha == "":
        notificar.config(fg = "red", text = "Todos os campos devem ser preenchidos!")
        return 

    for cpf_arquivo in todas_contas:
        if cpf == cpf_arquivo:
            notificar.config(fg = "red", text = "Conta já existente!")
            return
        else:
            novo_arquivo = open(cpf,"w")
            novo_arquivo.write(nome + "\t")
            novo_arquivo.write(idade + "\t")
            novo_arquivo.write(cpf + "\t")
            novo_arquivo.write(senha + "\t")
            novo_arquivo.write("0\n")

            notificar.config(fg = "green", text = "Conta criada com sucesso!")
               
def registro():

    global nome_temp
    global idade_temp
    global cpf_temp
    global senha_temp
    global notificar

    nome_temp = StringVar()
    idade_temp = StringVar()
    cpf_temp = StringVar()
    senha_temp = StringVar()

    tela_registro = Toplevel(master)
    tela_registro.title("Registro")

    Label(tela_registro, text = "Insira seus dados abaixo para o registro",font = fonte_padrao).grid(row = 0, sticky = N,pady = 10)
    Label(tela_registro, text = "Nome", font = fonte_padrao).grid(row = 1,sticky = W)
    Label(tela_registro, text = "Idade", font = fonte_padrao).grid(row = 2,sticky = W)
    Label(tela_registro, text = "CPF", font = fonte_padrao).grid(row = 3,sticky = W)
    Label(tela_registro, text = "Senha", font = fonte_padrao).grid(row = 4,sticky = W)
    notificar = Label(tela_registro, font = fonte_padrao)
    notificar.grid(row = 6, sticky = N, pady = 10)

    Entry(tela_registro, textvariable = nome_temp).grid(row = 1, column = 0)
    Entry(tela_registro, textvariable = idade_temp).grid(row = 2, column = 0)
    Entry(tela_registro, textvariable = cpf_temp).grid(row = 3, column = 0)
    Entry(tela_registro, textvariable = senha_temp, show = "*").grid(row = 4, column = 0)

    Button(tela_registro, text = "Registrar", font = fonte_padrao, command = terminar_reg).grid(row = 5, sticky = N, pady = 10)

def sessao_login():

    global cpf_login
    global senha_login

    todas_contas = os.listdir()
    cpf_login = cpf_login_temp.get()
    senha_login = senha_login_temp.get()

    for cpf in todas_contas:
        if cpf == cpf_login:
            file = open(cpf,"r")
            dados_file = file.read()
            dados_file = dados_file.split("\t")
            senha = dados_file[3]
            if senha_login == senha:
                tela_login.destroy()
                dados_conta = Toplevel(master)
                dados_conta.title("Menu Conta")

                Label(dados_conta,text = "Menu Conta",font = fonte_padrao).grid(row = 0, sticky = N, pady = 10)
                Label(dados_conta, text = "Bem-vindo!", font = fonte_padrao).grid(row = 1, sticky = N, pady = 10)

                Button(dados_conta, text = "Detalhes", font = fonte_padrao, command = detalhes_conta).grid(row = 2, sticky = N, padx = 10)
                Button(dados_conta, text = "Depósito", font = fonte_padrao, command = depositar).grid(row = 3, sticky = N, padx = 10)
                Button(dados_conta, text = "Saque", font = fonte_padrao,command = sacar).grid(row = 4, sticky = N, padx = 10)
                Button(dados_conta, text = "Transferência", font = fonte_padrao, command = transferir).grid(row = 5, sticky = N, padx = 10)
                Label(dados_conta).grid(row = 6, sticky = N, pady = 10)

                return
            else:
                alerta_login.config(fg = "red", text = "Senha Incorreta!")
                return
    alerta_login.config(fg = "red", text = "Conta não registrada!")

def depositar():
    global valor
    global alerta_deposito
    global label_saldo_atual

    valor = StringVar()
    file = open(cpf_login,"r")
    dados_file = file.read()
    dados_usuario = dados_file.split("\t")
    saldo_usuario = dados_usuario[4]

    tela_deposito = Toplevel(master)
    tela_deposito.title("Depósito")
    Label(tela_deposito, text = "Depósito", font = fonte_padrao).grid(row = 0, sticky = N, pady = 10)
    label_saldo_atual = Label(tela_deposito, text = "Saldo Atual: R$" + saldo_usuario, font = fonte_padrao)
    label_saldo_atual.grid(row = 1, sticky = W)
    Label(tela_deposito, text = "Valor: R$", font = fonte_padrao).grid(row = 2, sticky = W)
    alerta_deposito = Label(tela_deposito, font = fonte_padrao)
    alerta_deposito.grid(row = 4, sticky = N , pady = 5)

    Entry(tela_deposito, textvariable = valor).grid(row = 2, column = 1)

    Button(tela_deposito, text = "Concluir", font = fonte_padrao, command = concluir_Deposito).grid(row = 3,column = 1, sticky = W, pady = 5)

def concluir_Deposito():
    if valor.get() == "":
        alerta_deposito.config( text = "O valor é requerido!", fg = "red")
    if float(valor.get()) <= 0:
        alerta_deposito.config(text = "Valores negativos não são aceitos!",fg = "red")
        return

    file = open(cpf_login, "r+")
    dados_file = file.read()
    dados = dados_file.split("\t")
    saldo_atual = dados[4]
    novo_saldo = saldo_atual
    novo_saldo = float(novo_saldo) + float(valor.get())
    dados_file = dados_file.replace(saldo_atual, str(format("%.2f"%novo_saldo)))
    file.seek(0)
    file.truncate(0)
    file.write(dados_file)  
    file.close()

    label_saldo_atual.config(text = "Saldo Atual: R$" + str(format("%.2f"%novo_saldo)),fg = "green")
    alerta_deposito.config(text = "Depósito feito com sucesso!", fg = "green")

def sacar():
    global alerta_saque
    global valor_saque
    global label_saldo_atual

    valor_saque = StringVar()
    file = open(cpf_login,"r")
    dados_file = file.read()
    dados_usuario = dados_file.split("\t")
    saldo_usuario = dados_usuario[4]

    tela_saque = Toplevel(master)
    tela_saque.title("Saque")
    Label(tela_saque, text = "Saque", font = fonte_padrao).grid(row = 0, sticky = N, pady = 10)
    label_saldo_atual = Label(tela_saque, text = "Saldo Atual: R$" + saldo_usuario, font = fonte_padrao)
    label_saldo_atual.grid(row = 1, sticky = W)
    Label(tela_saque, text = "Valor: R$", font = fonte_padrao).grid(row = 2, sticky = W)
    alerta_saque = Label(tela_saque, font = fonte_padrao)
    alerta_saque.grid(row = 4, sticky = N , pady = 5)

    Entry(tela_saque, textvariable = valor_saque).grid(row = 2, column = 1)

    Button(tela_saque, text = "Concluir", font = fonte_padrao, command = concluir_Saque).grid(row = 3,column = 1, sticky = W, pady = 5)

def concluir_Saque():
    if valor_saque.get() == "":
        alerta_saque.config( text = "O valor é requerido!", fg = "red")
    if float(valor_saque.get()) <= 0.0:
        alerta_saque.config(text = "Valores negativos não são aceitos!",fg = "red")
        return

    file = open(cpf_login, "r+")
    dados_file = file.read()
    dados = dados_file.split("\t")
    saldo_atual = dados[4]

    if float(valor_saque.get()) > float(saldo_atual):
        alerta_saque.config(text = "Saldo Insuficiente!",fg = "red")
        return

    novo_saldo = saldo_atual
    novo_saldo = float(novo_saldo) - float(valor_saque.get())
    dados_file = dados_file.replace(saldo_atual, str(format("%.2f"%novo_saldo)))
    file.seek(0)
    file.truncate(0)
    file.write(dados_file)  
    file.close()

    label_saldo_atual.config(text = "Saldo Atual: R$" + str(format("%.2f"%novo_saldo)),fg = "green")
    alerta_saque.config(text = "Saque feito com sucesso!", fg = "green")

def transferir():

    file = open(cpf_login,"r")
    dados_file = file.read()
    dados_usuario = dados_file.split("\t")
    saldo_usuario = dados_usuario[4]

    global alerta_transferir
    global valor_transferir  
    global cpf_transferir
    global label_saldo_atual_trans

    cpf_transferir = StringVar()
    valor_transferir = StringVar()

    tela_transferencia = Toplevel(master)
    tela_transferencia.title("Transferência")

    Label(tela_transferencia, text = "Insira o dados a seguir", font = fonte_padrao).grid(row = 0, sticky = N, pady = 10)
    label_saldo_atual_trans = Label(tela_transferencia, text = "Saldo Atual: R$" + saldo_usuario, font = fonte_padrao)
    label_saldo_atual_trans.grid(row = 1, sticky = W)
    Label(tela_transferencia, text = "CPF (Conta destino)", font = fonte_padrao).grid(row = 2, sticky = W)
    Label(tela_transferencia, text = "Valor: R$", font = fonte_padrao).grid(row = 3, sticky = W)
    alerta_transferir = Label(tela_transferencia, font = fonte_padrao)
    alerta_transferir.grid(row = 4, sticky = N)

    Entry(tela_transferencia, textvariable = cpf_transferir).grid(row = 2, column = 1, padx = 5)
    Entry(tela_transferencia, textvariable = valor_transferir).grid(row = 3, column = 1, padx = 5)
    
    Button(tela_transferencia, text = "Transferir", command = concluir_transferencia, width = 15,font = fonte_padrao).grid(row = 4, column = 1, pady = 5, padx = 5)

def concluir_transferencia():
    cpf_trans = cpf_transferir.get()

    if valor_transferir.get() == "":
        alerta_transferir.config(text = "O valor é requerido!", fg = "red")
    if float(valor_transferir.get()) <= 0.0:
        alerta_transferir.config(text = "Valores negativos não são aceitos!",fg = "red")
        return

    try:
        if cpf_trans != "" and cpf_trans != cpf_login:
           file = open(cpf_trans,"r+")
           dados_file = file.read()
           dados = dados_file.split("\t")
           saldo_atual = dados[4]
           novo_saldo = saldo_atual

           file2 = open(cpf_login,"r+")
           dados_file2 = file2.read()
           dados2 = dados_file2.split("\t")
           saldo_atual2 = dados2[4]

           if float(valor_transferir.get()) > float(saldo_atual2):
                alerta_transferir.config(text = "Saldo Insuficiente!",fg = "red")
                return

           novo_saldo2 = saldo_atual2
           novo_saldo2 = float(novo_saldo2) - float(valor_transferir.get())
           dados_file2 = dados_file2.replace(saldo_atual2, str(format("%.2f"%novo_saldo2)))
           file2.seek(0)
           file2.truncate(0)
           file2.write(dados_file2)
           file2.close()

           novo_saldo = float(novo_saldo) + float(valor_transferir.get())
           dados_file = dados_file.replace(saldo_atual, str(format("%.2f"%novo_saldo)))
           file.seek(0)
           file.truncate(0)
           file.write(dados_file)
           file.close()

           label_saldo_atual_trans.config(text = "Saldo Atual (Conta Receptora): R$" + str(format("%.2f"%novo_saldo)) + "\n" + "Saldo Atual (Conta Emissora): R$" + str(format("%.2f"%novo_saldo2)),fg = "green")
           alerta_transferir.config(text = "Transferência feita com sucesso!", fg = "green")
           return
        else:
            alerta_transferir.config(fg = "red",text = "Campo obrigatório! Insira o CPF destino!")
            return
    except FileNotFoundError:
        alerta_transferir.config(fg = "red",text = "CPF não registrado!")
    

def detalhes_conta():
    file = open(cpf_login, "r")
    dados_file = file.read()
    dados_usuario = dados_file.split("\t")
    nome_usuario = dados_usuario[0]
    idade_usuario = dados_usuario[1]
    cpf_usuario = dados_usuario[2]
    senha_usuario = dados_usuario[3]
    saldo_usuario = dados_usuario[4]


    tela_detalhes_conta = Toplevel(master)
    tela_detalhes_conta.title("Detalhes da Conta")

    Label(tela_detalhes_conta, text = "Detalhes da Conta: ", font = fonte_padrao).grid(row = 0, sticky = N, pady = 10)
    Label(tela_detalhes_conta, text = "Nome:  " + nome_usuario, font = fonte_padrao).grid(row = 1, sticky = W)
    Label(tela_detalhes_conta, text = "Idade: " + idade_usuario, font = fonte_padrao).grid(row = 2, sticky = W)
    Label(tela_detalhes_conta, text = "CPF: " + cpf_usuario, font = fonte_padrao).grid(row = 3, sticky = W)
    Label(tela_detalhes_conta, text = "Senha: " + senha_usuario, font = fonte_padrao).grid(row = 4, sticky = W)
    Label(tela_detalhes_conta, text = "Saldo: R$" + saldo_usuario, font = fonte_padrao).grid(row = 5, sticky = W)

def login():

    global cpf_login_temp
    global alerta_login
    global senha_login_temp
    global tela_login

    cpf_login_temp = StringVar()
    senha_login_temp = StringVar()

    tela_login = Toplevel(master)
    tela_login.title("Login")

    Label(tela_login, text = "Entre em sua conta",font = fonte_padrao).grid(row = 0, sticky = N, pady = 10)
    Label(tela_login, text = "CPF",font = fonte_padrao).grid(row = 1, sticky = W)
    Label(tela_login, text = "Senha ",font = fonte_padrao).grid(row = 2, sticky = W)
    alerta_login = Label(tela_login, font = fonte_padrao)
    alerta_login.grid(row = 4, sticky = N)

    Entry(tela_login,textvariable = cpf_login_temp).grid(row = 1, column = 1, padx = 5)
    Entry(tela_login, textvariable = senha_login_temp,show = "*").grid(row = 2, column = 1, padx = 5)

    Button(tela_login, text = "Login", command = sessao_login, width = 15,font = fonte_padrao).grid(row = 3, column = 1, pady = 5, padx = 5)

Label(master,text = "Gerenciador de Contas", font = ("Calibri",13)).grid(row = 0, sticky = N, pady = 10)

Button(master, text = "Registrar", font = fonte_padrao,command = registro, width = 10).grid(row = 3, sticky = N)
Button(master, text = "Login", font = fonte_padrao,command = login,  width = 10).grid(row = 4, sticky = N, pady = 10)

master.mainloop()