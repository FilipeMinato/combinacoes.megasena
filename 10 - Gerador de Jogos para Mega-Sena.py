import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import random

"""
Este programa é um Gerador de Jogos da Mega-Sena com interface gráfica usando Tkinter.
Ele permite ao usuário:
- Escolher a quantidade de jogos e dezenas por jogo (entre 6 e 15);
- Selecionar dezenas fixas (que sempre estarão nos jogos);
- Selecionar dezenas excluídas (que nunca aparecerão);
- Gerar os jogos com base nessas configurações;
- Ver as estatísticas de cada jogo (pares, ímpares, soma dos números);
- Confirmar o custo total antes de gerar.

Todos os jogos são exibidos em uma área de texto com rolagem.
"""

# Preços oficiais da Mega-Sena de acordo com a quantidade de dezenas por jogo
preco_por_dezena = {
    6: 5.00, 7: 35.00, 8: 140.00, 9: 420.00, 10: 1050.00,
    11: 2310.00, 12: 4620.00, 13: 8580.00, 14: 15015.00, 15: 25025.00
}


def calcular_estatisticas(jogo):
    """Recebe uma lista de dezenas e calcula:
       - Quantidade de pares
       - Quantidade de ímpares
       - Soma total dos números
    """
    pares = sum(1 for n in jogo if n % 2 == 0)
    impares = len(jogo) - pares
    soma = sum(jogo)
    return pares, impares, soma


def gerar_jogo(fixas, excluidas, dezenas_por_jogo):
    """Gera um jogo aleatório com base nas dezenas fixas e excluídas."""
    jogo = fixas.copy()
    while len(jogo) < dezenas_por_jogo:
        n = random.randint(1, 60)
        if n not in jogo and n not in excluidas:
            jogo.append(n)
    return sorted(jogo)


def adicionar_dezenas(titulo, destino, bloqueadas=[]):
    """
    Abre uma caixa de diálogo para o usuário inserir dezenas (fixas ou excluídas).
    `destino`: lista onde as dezenas serão armazenadas.
    `bloqueadas`: dezenas que não podem ser escolhidas (evita conflito entre fixas e excluídas).
    """
    dezenas = []
    while True:
        try:
            d = simpledialog.askinteger(titulo, "Digite uma dezena (1 a 60). 0 para parar:")
            if d == 0:
                break
            if 1 <= d <= 60 and d not in dezenas and d not in bloqueadas:
                dezenas.append(d)
            else:
                messagebox.showwarning("Inválido", "Dezena repetida ou não permitida.")
        except:
            break
    destino.clear()
    destino.extend(dezenas)


def gerar_jogos():
    """Função principal para gerar os jogos após preenchimento dos campos e confirmação."""
    try:
        qtd = int(entry_qtd.get())
        dezenas = int(entry_dezenas.get())
        if dezenas not in preco_por_dezena:
            raise ValueError
    except:
        messagebox.showerror("Erro", "Preencha corretamente a quantidade e as dezenas (6 a 15).")
        return

    # Calcula o valor total da aposta
    valor_total = qtd * preco_por_dezena[dezenas]

    # Confirmação do valor total antes de gerar os jogos
    confirmar = messagebox.askyesno("Confirmar",
                                    f"{qtd} jogos de {dezenas} dezenas\nTotal: R$ {valor_total:.2f}\nDeseja continuar?")
    if not confirmar:
        return

    resultado.delete("1.0", tk.END)
    todos.clear()

    for i in range(1, qtd + 1):
        jogo = gerar_jogo(fixas, excluidas, dezenas)

        # Evita jogos repetidos
        if jogo in todos:
            i -= 1
            continue

        todos.append(jogo)
        pares, impares, soma = calcular_estatisticas(jogo)
        resultado.insert(tk.END, f"Jogo {i}: {jogo} | Pares: {pares} | Ímpares: {impares} | Soma: {soma}\n")


# ========== Interface Gráfica ==========

# Janela principal
root = tk.Tk()
root.title("Gerador de Jogos da Mega-Sena")
root.geometry("550x600")

# Listas que armazenam dezenas fixas, excluídas e jogos gerados
fixas = []
excluidas = []
todos = []

# Entrada da quantidade de jogos
tk.Label(root, text="Quantos jogos deseja gerar?").pack()
entry_qtd = tk.Entry(root)
entry_qtd.pack(pady=5)

# Entrada da quantidade de dezenas por jogo
tk.Label(root, text="Quantas dezenas por jogo? (6 a 15)").pack()
entry_dezenas = tk.Entry(root)
entry_dezenas.pack(pady=5)

# Botões para selecionar dezenas fixas e excluídas
tk.Button(root, text="Selecionar Dezenas Fixas",
          command=lambda: adicionar_dezenas("Fixar Dezenas", fixas, excluidas)).pack(pady=5)
tk.Button(root, text="Selecionar Dezenas Excluídas",
          command=lambda: adicionar_dezenas("Excluir Dezenas", excluidas, fixas)).pack(pady=5)

# Botão principal para gerar os jogos
tk.Button(root, text="Gerar Jogos", bg="green", fg="white", font=("Arial", 12), command=gerar_jogos).pack(pady=10)

# Área de resultados com barra de rolagem
resultado = scrolledtext.ScrolledText(root, height=20, width=65)
resultado.pack(pady=10)

# Aviso ao final
tk.Label(root, text="Observação: Os jogos gerados são aleatórios e não garantem premiação.").pack(pady=5)

# Inicia a interface
root.mainloop()
