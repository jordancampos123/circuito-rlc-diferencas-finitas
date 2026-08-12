import numpy as np
import matplotlib.pyplot as plt

# Parâmetros elétricos
R = 20.0
L = 10.0
C = 0.004

# Condições iniciais
v0 = 0.0
vp0 = -1125.0

# Intervalo temporal
t0 = 0.0
tf = 3.0

# Passo de referência
h_ref = 0.01

# Passos analisados no refinamento da malha
# Para testar outros valores, altere somente esta lista.
h_values = [0.02, 0.01, 0.005, 0.0025]

def solucao_analitica(t):
    """Retorna a solução analítica do circuito RLC estudado."""
    return 150.0 * (np.exp(-10.0 * t) - np.exp(-2.5 * t))


def diferencas_finitas(h):
    """Calcula a solução numérica e o erro absoluto para um passo temporal h."""
    n_pontos = int(round((tf - t0) / h)) + 1
    t = t0 + np.arange(n_pontos) * h

    v = np.zeros(n_pontos)
    v[0] = v0
    v[1] = v0 + h * vp0

    A = 2.0 - (h**2) / (L * C)
    B = 1.0 - h / (2.0 * R * C)
    D = 1.0 + h / (2.0 * R * C)

    for i in range(1, n_pontos - 1):
        v[i + 1] = (A * v[i] - B * v[i - 1]) / D

    v_exata = solucao_analitica(t)
    erro = np.abs(v - v_exata)

    return t, v, v_exata, erro

t_ref, v_ref, v_exata_ref, erro_ref = diferencas_finitas(h_ref)

tempos_tabela = [0.00, 0.10, 0.20, 0.50, 1.00, 1.50, 2.00, 2.50, 3.00]

print(
    f"{'Tempo (s)':<12}"
    f"{'Solução numérica (V)':<24}"
    f"{'Solução analítica (V)':<25}"
    f"{'Erro absoluto (V)':<20}"
)
print("-" * 81)

for tempo in tempos_tabela:
    indice = int(round((tempo - t0) / h_ref))

    print(
        f"{t_ref[indice]:<12.2f}"
        f"{v_ref[indice]:<24.6f}"
        f"{v_exata_ref[indice]:<25.6f}"
        f"{erro_ref[indice]:<20.6f}"
    )

resultados = {}

for h in h_values:
    t_h, v_h, v_exata_h, erro_h = diferencas_finitas(h)

    resultados[h] = {
        "t": t_h,
        "v": v_h,
        "v_exata": v_exata_h,
        "erro": erro_h,
        "erro_maximo": np.max(erro_h),
        "erro_medio": np.mean(erro_h),
    }

plt.figure(figsize=(10, 6))

for h in h_values:
    plt.plot(
        resultados[h]["t"],
        resultados[h]["v"],
        linewidth=1.5,
        label=f"MDF - h = {h:g}",
    )

t_exato = np.linspace(t0, tf, 2000)

plt.plot(
    t_exato,
    solucao_analitica(t_exato),
    "--",
    linewidth=2.5,
    label="Solução analítica",
)

plt.xlabel("Tempo (s)")
plt.ylabel("Tensão (V)")
plt.title("Comparação das soluções para diferentes valores de h")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

for h in h_values:
    plt.plot(
        resultados[h]["t"],
        resultados[h]["erro"],
        linewidth=1.5,
        label=f"h = {h:g}",
    )

plt.xlabel("Tempo (s)")
plt.ylabel("Erro absoluto (V)")
plt.title("Erro absoluto para diferentes valores de h")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print(
    f"{'h (s)':<12}"
    f"{'Erro máximo (V)':<22}"
    f"{'Erro médio (V)':<22}"
)
print("-" * 56)

for h in h_values:
    print(
        f"{h:<12.4f}"
        f"{resultados[h]['erro_maximo']:<22.8f}"
        f"{resultados[h]['erro_medio']:<22.8f}"
    )

print(
    f"{'Refinamento de h':<28}"
    f"{'Razão dos erros máximos':<25}"
)
print("-" * 53)

for i in range(len(h_values) - 1):
    h_atual = h_values[i]
    h_seguinte = h_values[i + 1]

    razao = (
        resultados[h_atual]["erro_maximo"]
        / resultados[h_seguinte]["erro_maximo"]
    )

    print(
        f"{h_atual:.4f} -> {h_seguinte:.4f}"
        f"{'':<10}"
        f"{razao:.4f}"
    )
