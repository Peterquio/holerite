import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys

# === AJUSTE DE CAMINHO PARA FUNCIONAR NO .EXE ===
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(APP_DIR, "aliquotas.json")

# === FUNÇÕES DE CÁLCULO ===
def carregar_aliquotas():
    if not os.path.exists(CONFIG_FILE):
        messagebox.showerror("Erro", f"O arquivo de alíquotas não foi encontrado:\n{CONFIG_FILE}")
        root.destroy()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def calcular_inss(bruto, inss_tabela):
    for faixa in inss_tabela:
        minimo = faixa["min"]
        maximo = faixa["max"]
        aliquota = faixa["aliquota"]
        deducao = faixa["deducao"]

        if maximo is None:  # teto
            return round(deducao, 2)

        if minimo <= bruto <= maximo:
            if aliquota is not None:
                return round(bruto * aliquota - deducao, 2)
            else:
                return round(deducao, 2)

    return 0.0

def calcular_irrf(bruto, faixas_irrf):
    base = bruto - 607.20
    if base <= 0:
        return 0.0

    for faixa in faixas_irrf:
        minimo = faixa["min"]
        maximo = faixa["max"]
        aliquota = faixa["aliquota"]
        deducao = faixa["deducao"]

        if maximo is None or (minimo <= base <= maximo):
            valor = base * aliquota - deducao
            return round(valor if valor > 0 else 0, 2)

    return 0.0

# === INTERFACE ===
def calcular():
    total_ganhos = 0
    total_descontos = 0

    for e in entradas_ganhos:
        try:
            total_ganhos += float(e.get())
        except:
            pass

    for e in entradas_descontos:
        try:
            total_descontos += float(e.get())
        except:
            pass

    if total_ganhos == 0:
        messagebox.showwarning("Aviso", "Nenhum valor de ganho informado!")
        return

    # Calcular INSS e IRRF
    inss = calcular_inss(total_ganhos, aliquotas["INSS"])
    irrf = calcular_irrf(total_ganhos, aliquotas["IRRF"])

    liquido = total_ganhos - total_descontos - inss - irrf

    resultado.set(
        f"Total Ganhos: R$ {total_ganhos:.2f}\n"
        f"Total Descontos: R$ {total_descontos:.2f}\n"
        f"INSS: R$ {inss:.2f}\n"
        f"IRRF: R$ {irrf:.2f}\n"
        f"Salário Líquido: R$ {liquido:.2f}"
    )

def adicionar_linha():
    e1 = tk.Entry(frame_ganhos, width=20)
    e1.grid(row=len(entradas_ganhos), column=0, padx=5, pady=2)
    entradas_ganhos.append(e1)

    e2 = tk.Entry(frame_descontos, width=20)
    e2.grid(row=len(entradas_descontos), column=0, padx=5, pady=2)
    entradas_descontos.append(e2)

# === MAIN ===
root = tk.Tk()
root.title("Calculadora de Holerite - Peterquio")

# Carregar alíquotas
aliquotas = carregar_aliquotas()

frame = ttk.Frame(root, padding=10)
frame.pack()

frame_ganhos = ttk.LabelFrame(frame, text="Ganhos")
frame_ganhos.grid(row=0, column=0, padx=10, pady=5)

frame_descontos = ttk.LabelFrame(frame, text="Descontos")
frame_descontos.grid(row=0, column=1, padx=10, pady=5)

entradas_ganhos = []
entradas_descontos = []

for _ in range(3):
    adicionar_linha()

btn_add = ttk.Button(frame, text="Adicionar Linha", command=adicionar_linha)
btn_add.grid(row=1, column=0, pady=10)

btn_calc = ttk.Button(frame, text="Calcular", command=calcular)
btn_calc.grid(row=1, column=1, pady=10)

resultado = tk.StringVar()
lbl_result = ttk.Label(frame, textvariable=resultado, justify="left")
lbl_result.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()