import json

# Arquivo para salvar alíquotas
CONFIG_FILE = "aliquotas.json"

def gerar_tabelas():
    # === TABELA IRRF ===
    irrf = [
        {"faixa": "Até 2428,80", "min": 0, "max": 2428.80, "aliquota": 0.00, "deducao": 0.00},
        {"faixa": "2428,81 até 2826,65", "min": 2428.81, "max": 2826.65, "aliquota": 0.075, "deducao": 182.16},
        {"faixa": "2826,66 até 3751,05", "min": 2826.66, "max": 3751.05, "aliquota": 0.15, "deducao": 394.16},
        {"faixa": "3751,06 até 4664,68", "min": 3751.06, "max": 4664.68, "aliquota": 0.225, "deducao": 675.49},
        {"faixa": "Acima de 4664,68", "min": 4664.69, "max": None, "aliquota": 0.275, "deducao": 908.73}
    ]

    # === TABELA INSS ===
    inss = [
        {"faixa": "Até 1518,00", "min": 0, "max": 1518.00, "aliquota": 0.075, "deducao": 0.00},
        {"faixa": "1518,01 até 2793,88", "min": 1518.01, "max": 2793.88, "aliquota": 0.09, "deducao": 22.77},
        {"faixa": "2793,89 até 4190,83", "min": 2793.89, "max": 4190.83, "aliquota": 0.12, "deducao": 106.59},
        {"faixa": "4190,84 até 8157,41", "min": 4190.84, "max": 8157.41, "aliquota": 0.14, "deducao": 190.40},
        {"faixa": "Acima de 8157,41", "min": 8157.42, "max": None, "aliquota": None, "deducao": 951.63}
    ]

    dados = {"IRRF": irrf, "INSS": inss}

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f"Tabelas salvas em {CONFIG_FILE}")

# === Executa a geração ===
if __name__ == "__main__":
    gerar_tabelas()
