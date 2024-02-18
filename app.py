from tkinter import ttk
from tkinter import *
import sqlite3

class Produto:
    db = 'database/produtos.db'

    def __init__(self, root):
        self.janela = root
        self.janela.title('App Gestor de Produtos') #Título da Janela
        self.janela.resizable(1,1) # Redimensiona a janela
        #self.janela.geometry('400x600') # Define a resolução em pixels da janela
        self.janela.wm_iconbitmap('recursos/icon.ico') # Altera o ícone da janela

        frame = LabelFrame(self.janela, text="Registar um novo Produto",font=('Calibri', 16, 'bold')) # Cria um frame na janela e da-o um título
        frame.grid(row=0, column=0, columnspan=3, pady=20) # Especifica os limites do grid do frame criado
        frame.columnconfigure(1, weight=1)  # Permite a expansão da coluna 1

        self.etiqueta_nome = Label(frame, text="Nome: ",font=('Calibri', 13))  # CRIA A ETIQUETA 'NOME' DENTRO DO FRAME
        self.etiqueta_nome.grid(row=1, column=0) #POSICIONA O GRID DA ETIQUETA 'NOME' DENTRO DO FRAME
        self.nome = Entry(frame) #CRIA O INPUT PARA O UTILIZADOR
        self.nome.focus() #FAZ COM QUE O INPUT ESTEJA O WIDGET 'ATIVO' AO ABRIR-SE A JANELA
        self.nome.grid(row=1, column=1, sticky='ew') #POSICIONA O INPUT

        self.etiqueta_preço = Label(frame, text="Preço: ",font=('Calibri', 13))  # CRIA A ETIQUETA 'PREÇO' DENTRO DO FRAME
        self.etiqueta_preço.grid(row=2, column=0) # POSICIONA O GRID DA ETIQUETA DENTRO DO FRAME
        self.preco = Entry(frame) #CRIA O INPUT PARA INSERÇÃO DO PREÇO
        self.preco.grid(row=2, column=1, sticky = 'ew') #POSICIONA A ETIQUETA DO PREÇO DENTRO DO FRAME

        # Botão Adicionar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_adicionar = ttk.Button(frame, text="Guardar Produto", command=self.add_produto,style='my.TButton')
        self.botao_adicionar.grid(row=3, columnspan=2,sticky= W + E)
        # Adicionando mensagem informativa ao utilizador
        self.mensagem = Label(text='', fg='red')
        self.mensagem.grid(row=3, column=0, columnspan=2, sticky=W + E)


        #Botao Eliminar e Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        botão_eliminar = ttk.Button(text='ELIMINAR' , command = self.del_produto,style='my.TButton')
        botão_eliminar.grid(row=5, column=0, sticky=W + E)
        botão_editar = ttk.Button(text='EDITAR' , command = self.edit_produto,style='my.TButton')
        botão_editar.grid(row=5, column=1, sticky=W + E)


        # TABELA DE PRODUTOS
        style = ttk.Style()
        # Modifica a fonte da tabela
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',11))
        # Modifica a fonte da cabeceira
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # ESTRUTURA DA TABELA
        self.tabela = ttk.Treeview(height=16, columns=2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column=0, columnspan=2, pady = 0)
        self.tabela.heading('#0', text='Nome', anchor=CENTER)  # Cabeçalho 0
        self.tabela.heading('#1', text='Preço', anchor=CENTER)  # Cabeçalho 1

        self.get_produtos()
    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con: # Incia uma conexão com a base de dados
            cursor = con.cursor() # Cria o cursor para navegar na BD
            resultado = cursor.execute(consulta, parametros) #Prepara a consulta com os parâmetros
            con.commit() #Executa a consulta antes preparada
        return resultado #Retorna o resultado da consulta

    def get_produtos(self):
        registos_tabela = self.tabela.get_children()  # Obter todos os dados da tabela
        for linha in registos_tabela:
            self.tabela.delete(linha)

        query = 'SELECT * FROM produto ORDER BY nome DESC' # Cria uma lista com todos os produtos, ord p/ nome
        registos = self.db_consulta(query)  # Faz-se a chamada ao método db_consultas

        # Escrever os dados no ecrã
        for linha in registos:
            print(linha)  # print para verificar por consola os dados
            self.tabela.insert('', 0, text=linha[1], values=linha[2])

    def validacao_nome(self): # Valida o dado inserido pelo utlizador no campo 'nome'
        nome_introduzido_por_utilizador = self.nome.get()
        return len(nome_introduzido_por_utilizador) != 0 # Garante que o campo não esteja vazio

    def validacao_preco(self): # Valida o dado inserido pelo utlizador no campo 'preço'
        preco_introduzido_por_utilizador = self.preco.get()
        return len(preco_introduzido_por_utilizador) != 0

    def add_produto(self):
        if self.validacao_nome() and self.validacao_preco(): #Imprime nome e preço se forem preenchidos corretamente
            query = 'INSERT INTO produto VALUES(NULL, ?, ?)'  # Consulta SQL (sem os dados)
            parametros = (self.nome.get(), self.preco.get())  # Parâmetros da consulta SQL
            self.db_consulta(query, parametros)
            print("Dados guardados")
            self.mensagem['text'] = 'Produto {} adicionado com êxito'.format(self.nome.get()) # Label localizada entre o botão e a tabela
            self.nome.delete(0, END)  # Apagar o campo nome do formulário
            self.preco.delete(0, END)  # Apagar o campo preço do formulário

        elif self.validacao_nome() and self.validacao_preco() == False:
            print("O preço é obrigatório")
            self.mensagem['text'] = 'O preço é obrigatório'
        elif self.validacao_nome() == False and self.validacao_preco():
            print("O nome é obrigatório")
            self.mensagem['text'] = 'O nome é obrigatório'
        else:
            print("O nome e o preço são obrigatórios")
            self.mensagem['text'] = 'O nome e o preço são obrigatórios'
        self.get_produtos() # Volta a invocar este método para atualizar o conteúdo e ver as alterações

    def del_produto(self):
        # Debug
        #print(self.tabela.item(self.tabela.selection()))
        #print(self.tabela.item(self.tabela.selection())['text'])
        #print(self.tabela.item(self.tabela.selection())['values'])
        #print(self.tabela.item(self.tabela.selection())['values'][0])

        self.mensagem['text'] = ''  # Mensagem inicialmente vazio
        # Comprovação de que se selecione um produto para poder eliminá-lo
        if not self.tabela.selection():
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return

        self.mensagem['text'] = ''
        nome = self.tabela.item(self.tabela.selection())['text']
        query = 'DELETE FROM produto WHERE nome = ?'  # Consulta SQL
        self.db_consulta(query, (nome,))  # Executar a consulta
        self.mensagem['text'] = f'Produto {nome} eliminado com êxito'
        self.get_produtos()  # Atualizar a tabela de produtos

    def edit_produto(self):
        self.mensagem['text'] = '' # Mensagem inicialmente vazia
        if not self.tabela.selection():
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return

        nome = self.tabela.item(self.tabela.selection())['text']
        old_preco = self.tabela.item(self.tabela.selection())['values'][0] # O preço encontra-se dentro de uma lista
        self.janela_editar = Toplevel() # Criar uma janela à frente da principal
        self.janela_editar.title = "Editar Produto" # Titulo da janela
        self.janela_editar.resizable(1, 1) # Ativar a redimensão da janela. Para desativá-la: (0,0)
        #self.janela_editar.geometry('550x250')  # Define a resolução em pixels da janela
        self.janela_editar.wm_iconbitmap('recursos/icon.ico') # Ícone da janela

        título = Label(self.janela_editar, text='Edição de Produtos',font=('Calibri', 50, 'bold'))
        título.grid(column=0, row=0)

        # Criação do recipiente Frame da janela de Editar Produto
        frame_ep = LabelFrame(self.janela_editar, text="Editar o seguinte Produto",font=('Calibri', 16, 'bold')) # frame_ep: Frame Editar Produto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nome antigo
        self.etiqueta_nome_antigo = Label(frame_ep, text="Nome antigo: ",font=('Calibri', 13))  # Etiqueta de texto localizada no frame
        self.etiqueta_nome_antigo.grid(row=2, column=0)  # Posicionamento através de grid
        # Entry Nome antigo (texto que não se poderá modificar)
        self.input_nome_antigo = Entry(frame_ep,textvariable=StringVar(self.janela_editar, value=nome), state='readonly')
        self.input_nome_antigo.grid(row=2, column=1)

        # Label Nome novo
        self.etiqueta_nome_novo = Label(frame_ep, text="Nome novo: ",font=('Calibri', 13)
)
        self.etiqueta_nome_novo.grid(row=3, column=0)
        # Entry Nome novo (texto que se poderá modificar)
        self.input_nome_novo = Entry(frame_ep)
        self.input_nome_novo.grid(row=3, column=1)
        self.input_nome_novo.focus()  # Para que a seta do rato vá a esta Entry ao início

        # Label Preço antigo
        self.etiqueta_preco_antigo = Label(frame_ep, text="Preço antigo: ",font=('Calibri', 13))  # Etiqueta de texto localizada no frame
        self.etiqueta_preco_antigo.grid(row=4, column=0)  # Posicionamento através de grid
        self.input_preco_antigo = Entry(frame_ep,textvariable=StringVar(self.janela_editar, value=old_preco),state='readonly')
        self.input_preco_antigo.grid(row=4, column=1)

        # Label Preço novo
        self.etiqueta_preco_novo = Label(frame_ep, text="Preço novo: ",font=('Calibri', 13))
        self.etiqueta_preco_novo.grid(row=5, column=0)
        # Entry Preço novo (texto que se poderá modificar)
        self.input_preco_novo = Entry(frame_ep)
        self.input_preco_novo.grid(row=5, column=1)

        # Botão Atualizar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))




        # Entry Preço novo (texto que se poderá modificar)
        self.input_preco_novo = Entry(frame_ep)
        self.input_preco_novo.grid(row=5, column=1)

        # Botão Atualizar Produto
        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto",
                                          style='my.TButton',
                                          command=lambda:
                                          self.atualizar_produtos(self.input_nome_novo.get(),
                                                                  self.input_nome_antigo.get(),
                                                                  self.input_preco_novo.get(),
                                                                  self.input_preco_antigo.get()))
        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)
        self.etiqueta_preco_novo.grid(row=5, column=0)

    def atualizar_produtos(self, novo_nome, antigo_nome, novo_preco, antigo_preco):
        produto_modificado = False
        query = 'UPDATE produto SET nome = ?, preco = ? WHERE nome = ? AND preco = ?'
        if novo_nome != '' and novo_preco != '':
            # Se o utilizador escreve novo nome e novo preço, mudam-se ambos
            parametros = (novo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome != '' and novo_preco == '':
            # Se o utilizador deixa vazio o novo preço, mantém-se o preço anterior
            parametros = (novo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome == '' and novo_preco != '':
            parametros = (antigo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True

        if (produto_modificado):
            self.db_consulta(query, parametros)  # Executar a consulta
            self.janela_editar.destroy()  # Fechar a janela de edição de produtos
            self.mensagem['text'] = 'O produto {} foi atualizado com êxito'.format(antigo_nome)  # Mostrar mensagem para o utilizador
            self.get_produtos()  # Atualizar a tabela de produtos
        else:
            self.janela_editar.destroy()  # Fechar a janela de edição de produtos
            self.mensagem['text'] = 'O produto {} NÃO foi atualizado'.format(antigo_nome)


if __name__ == '__main__':
    root = Tk() #Inicia da janela principal
    app = Produto(root) # Envia para classe 'Produto' o controle sobre a janela root
    root.mainloop() # Começa o ciclo de aplicação
