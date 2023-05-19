import tkinter as tk
from PIL import ImageTk, Image
import random
from datetime import date

# Dados das cartas de tarot (exemplo)
cartas = [
    {"nome": "Carta 1", "imagem": "carta1.png", "significado": "Significado da Carta 1"},
    {"nome": "Carta 2", "imagem": "carta2.png", "significado": "Significado da Carta 2"},
    {"nome": "Carta 3", "imagem": "carta3.png", "significado": "Significado da Carta 3"},
    # Adicione aqui as informações das outras cartas
]

def obter_cartas_aleatorias():
    return random.sample(cartas, 3)

def gerar_leitura():
    cartas_selecionadas = obter_cartas_aleatorias()
    leitura = "Leitura Diária\n\n"
    
    for carta in cartas_selecionadas:
        leitura += f"{carta['nome']}: {carta['significado']}\n\n"
    
    return leitura

def exibir_leitura():
    leitura = gerar_leitura()
    texto_leitura.configure(state=tk.NORMAL)
    texto_leitura.delete("1.0", tk.END)
    texto_leitura.insert(tk.END, leitura)
    texto_leitura.configure(state=tk.DISABLED)

def verificar_data():
    data_atual = date.today().isoformat()
    
    with open("ultima_execucao.txt", "r+") as arquivo:
        ultima_execucao = arquivo.read().strip()
        
        if ultima_execucao != data_atual:
            arquivo.seek(0)
            arquivo.write(data_atual)
            arquivo.truncate()
            exibir_leitura()

# Criação da janela principal
janela = tk.Tk()
janela.title("Leitura Diária de Tarot")
janela.geometry("600x400")

# Criação do fundo de mesa de madeira
imagem_fundo = ImageTk.PhotoImage(Image.open("imgs/table.png"))
fundo = tk.Label(janela, image=imagem_fundo)
fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Criação dos espaços reservados para as cartas
cartas_selecionadas = obter_cartas_aleatorias()
espaco1 = tk.Label(janela)
espaco1.place(x=100, y=100)
imagem_carta1 = ImageTk.PhotoImage(Image.open(cartas_selecionadas[0]["imagem"]))
carta1 = tk.Label(espaco1, image=imagem_carta1)
carta1.pack()

espaco2 = tk.Label(janela)
espaco2.place(x=250, y=100)
imagem_carta2 = ImageTk.PhotoImage(Image.open(cartas_selecionadas[1]["imagem"]))
carta2 = tk.Label(espaco2, image=imagem_carta2)
carta2.pack()

espaco3 = tk.Label(janela)
espaco3.place(x=400, y=100)
imagem_carta3 = ImageTk.PhotoImage(Image.open(cartas_selecionadas[2]["imagem"]))
carta3 = tk.Label(espaco3, image=imagem_carta3)
carta3.pack()

# Botão para exibir a leitura
botao_leitura = tk.Button(janela, text="Exibir Leitura", command=verificar_data)
botao_leitura.place(x=260, y=300)

# Texto da leitura
texto_leitura = tk.Text(janela, width=40, height=10)
texto_leitura.place(x=180, y=150)
texto_leitura.configure(state=tk.DISABLED)

janela.mainloop()
