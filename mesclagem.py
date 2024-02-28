'''Estas são as bibliotecas que estamos importando. tkinter é a biblioteca para criar interfaces gráficas, PyPDF2
é utilizada para lidar com arquivos PDF, e os nos ajudará a lidar com operações do sistema operacional,
embora neste código específico não estejamos usando diretamente.'''

import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os

'''Aqui começamos a definir a classe PDFMergerApp, que representa nossa aplicação. O método __init__
é chamado quando uma instância da classe é criada. Aqui configuramos a janela principal da aplicação,
definindo o título, tamanho e inicializando uma lista vazia para armazenar as entradas de arquivos
selecionados. Criamos uma etiqueta (Label), uma caixa de entrada (Entry) e um botão (Button) para o
usuário inserir a quantidade de arquivos a mesclar.'''

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mesclar Arquivos PDF")
        self.root.geometry("640x480")
        self.arquivos_selecionados = []

        self.label_quantidade = tk.Label(root, text="Quantidade de Arquivos:")
        self.label_quantidade.pack()

        self.entry_quantidade = tk.Entry(root)
        self.entry_quantidade.pack()

        self.button_ok = tk.Button(root, text="OK", command=self.adicionar_caixas)
        self.button_ok.pack()

        '''Neste método adicionar_caixas, chamado quando o usuário clica no botão "OK",
        obtemos a quantidade de arquivos que o usuário deseja mesclar. Se for válido,
        removemos os elementos da entrada de quantidade e do botão "OK". Em seguida,
        iteramos sobre a quantidade de arquivos para criar etiquetas, entradas e botões
        de escolha de arquivo para cada arquivo a ser mesclado. Esses elementos são
        organizados em um quadro (Frame) e armazenados na lista arquivos_selecionados.
        Por fim, criamos um botão para mesclar os arquivos.'''

    def adicionar_caixas(self):
        quantidade = int(self.entry_quantidade.get())
        if quantidade <= 0:
            messagebox.showerror("Erro", "Por favor, insira um número válido maior que zero.")
            return

        self.label_quantidade.pack_forget()
        self.entry_quantidade.pack_forget()
        self.button_ok.pack_forget()

        for i in range(quantidade):
            frame = tk.Frame(root)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"Arquivo {i+1}:")
            label.pack(side=tk.LEFT)

            entry = tk.Entry(frame, state="disabled", width=50)
            entry.pack(side=tk.LEFT)

            button_escolher = tk.Button(frame, text="Escolher arquivo", command=lambda e=entry: self.escolher_arquivo(e))
            button_escolher.pack(side=tk.LEFT, padx=(10, 0))

            self.arquivos_selecionados.append(entry)

        self.button_mesclar = tk.Button(root, text="Mesclar arquivos", command=self.mesclar_pdf)
        self.button_mesclar.pack()

        '''Estes métodos escolher_arquivo e mesclar_pdf são responsáveis por lidar com a seleção de
        arquivos e mesclagem dos PDFs, respectivamente. O método escolher_arquivo é chamado quando
        o usuário clica no botão "Escolher arquivo" ao lado de cada entrada de arquivo. Ele abre
        uma caixa de diálogo para selecionar um arquivo PDF e insere o caminho do arquivo na
        entrada correspondente. O método mesclar_pdf é chamado quando o usuário clica no botão
        "Mesclar arquivos". Ele verifica se todos os arquivos foram selecionados, mescla os
        arquivos PDF, solicita ao usuário onde salvar o arquivo mesclado e, finalmente, fecha a aplicação.'''

    def escolher_arquivo(self, entry):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, filename)
            entry.config(state="readonly")

    def mesclar_pdf(self):
        # Verificar se todos os arquivos foram selecionados
        for entry in self.arquivos_selecionados:
            if not entry.get():
                messagebox.showerror("Erro", "Por favor, selecione todos os arquivos PDF.")
                return

        # Mesclar os arquivos PDF
        merger = PyPDF2.PdfMerger()
        for entry in self.arquivos_selecionados:
            merger.append(entry.get())

        # Salvar o arquivo mesclado
        output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_filename:
            with open(output_filename, "wb") as output_file:
                merger.write(output_file)
                messagebox.showinfo("Concluído", "Os arquivos foram mesclados com sucesso.")
                self.root.quit()

# Criar e iniciar a aplicação
root = tk.Tk()
app = PDFMergerApp(root)
root.mainloop()
