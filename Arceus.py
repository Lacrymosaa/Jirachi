import tkinter as tk
import os
from PIL import ImageTk, Image
import random
from datetime import date

# Dados das cartas de tarot (exemplo)
cartas = [
    {"nome": "Carta 1", "imagem": "imgs/1.png", "significado": "Significado da Carta 1"},
    {"nome": "Carta 2", "imagem": "imgs/2.png", "significado": "Significado da Carta 2"},
    {"nome": "Carta 3", "imagem": "imgs/3.png", "significado": "Significado da Carta 3"},
    # Adicione aqui as informações das outras cartas
]

def obter_cartas_aleatorias():
    return random.sample(cartas, 3)

def virar_carta(carta, label):
    frente = ImageTk.PhotoImage(Image.open(carta["imagem"]))
    label.configure(image=frente)
    label.image = frente
    mostrar_leitura(carta)
    # Desabilitar seleção após a primeira carta virada
    for l in label_cartas:
        l.unbind("<Button-1>")
        l.configure(cursor="arrow")

def mostrar_leitura(carta):
    janela_leitura = tk.Toplevel(janela)
    janela_leitura.title("Leitura da Carta")
    janela_leitura.geometry("400x300")
    texto_leitura = tk.Text(janela_leitura, width=40, height=10)
    texto_leitura.pack()
    texto_leitura.insert(tk.END, f"{carta['nome']}: {carta['significado']}\n")
    texto_leitura.configure(state=tk.DISABLED)

# Verificar se já foi selecionada uma carta hoje
def verificar_carta_selecionada():
    hoje = date.today()
    data_str = hoje.strftime("%Y-%m-%d")
    arquivo_existe = os.path.isfile("carta_selecionada.txt")
    if not arquivo_existe:
        # Criar o arquivo vazio caso não exista
        with open("carta_selecionada.txt", "w"):
            pass
    with open("carta_selecionada.txt", "r") as arquivo:
        data = arquivo.read()
    return data == data_str


# Marcar a carta como selecionada
def marcar_carta_selecionada():
    hoje = date.today()
    data_str = hoje.strftime("%Y-%m-%d")
    with open("carta_selecionada.txt", "w") as arquivo:
        arquivo.write(data_str)

# Criação da janela principal
janela = tk.Tk()
janela.title("Leitura Diária de Tarot")
janela.geometry("830x475")
janela.resizable(False, False)

# Criação do fundo de mesa de madeira
imagem_fundo = ImageTk.PhotoImage(Image.open("imgs/table.png"))
fundo = tk.Label(janela, image=imagem_fundo)
fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Verificar se a carta já foi selecionada hoje
if not verificar_carta_selecionada():
    # Criação das cartas
    cartas_aleatorias = obter_cartas_aleatorias()
    verso = ImageTk.PhotoImage(Image.open("imgs/back.png"))
    espaco_cartas = []
    label_cartas = []
    for i, carta in enumerate(cartas_aleatorias):
        espaco_carta = tk.Label(janela)
        espaco_carta.place(x=40 + (i * 285), y=150)
        espaco_cartas.append(espaco_carta)
        imagem_carta = Image.open(carta["imagem"])
        frente = ImageTk.PhotoImage(imagem_carta)
        label_carta = tk.Label(espaco_carta, image=verso)
        label_carta.pack()
        label_cartas.append(label_carta)
        label_carta.bind("<Button-1>", lambda event, c=carta, l=label_carta: virar_carta(c, l))

    # Marcar a carta como selecionada
    marcar_carta_selecionada()



janela.mainloop()
