import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

# ── Функція та межі ──────────────────────────────────────────────────────────
def f(x):
    return x ** 2

a, b = 0, 2          # межі інтегрування
N = 1_000_000        # кількість випадкових точок

# ── Метод Монте-Карло ────────────────────────────────────────────────────────
np.random.seed(42)
x_rand = np.random.uniform(a, b, N)
monte_carlo_result = (b - a) * np.mean(f(x_rand))

# ── Аналітичне значення та quad ──────────────────────────────────────────────
analytical_result = (b**3 - a**3) / 3          # ∫x² dx = x³/3
quad_result, quad_error = spi.quad(f, a, b)

# ── Виведення результатів ────────────────────────────────────────────────────
print("=" * 50)
print(f"  Метод Монте-Карло  : {monte_carlo_result:.6f}  (N = {N:,})")
print(f"  scipy.integrate    : {quad_result:.6f}  (похибка ≈ {quad_error:.2e})")
print(f"  Аналітично         : {analytical_result:.6f}")
print("-" * 50)
print(f"  Відхилення МК від quad : {abs(monte_carlo_result - quad_result):.6f}")
print(f"  Відхилення МК від аналіт.: {abs(monte_carlo_result - analytical_result):.6f}")
print("=" * 50)

# ── Графік ───────────────────────────────────────────────────────────────────
x_plot = np.linspace(-0.5, 2.5, 400)
y_plot = f(x_plot)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Метод Монте-Карло: ∫₀² x² dx", fontsize=14, fontweight="bold")

# ---- Лівий: класичний графік із заповненою областю ----
ax1 = axes[0]
ax1.plot(x_plot, y_plot, "r", linewidth=2, label="f(x) = x²")
ix = np.linspace(a, b)
ax1.fill_between(ix, f(ix), color="gray", alpha=0.35, label="Площа інтеграла")
ax1.axvline(x=a, color="gray", linestyle="--", linewidth=1)
ax1.axvline(x=b, color="gray", linestyle="--", linewidth=1)
ax1.set_xlim([x_plot[0], x_plot[-1]])
ax1.set_ylim([0, max(y_plot) + 0.2])
ax1.set_xlabel("x"); ax1.set_ylabel("f(x)")
ax1.set_title("Графік функції та область інтегрування")
ax1.legend(); ax1.grid(alpha=0.4)

# ---- Правий: точки Монте-Карло (підвибірка 5000 для візуалізації) ----
ax2 = axes[1]
n_vis = 5000
x_vis = np.random.uniform(a, b, n_vis)
y_max = f(b)
y_vis = np.random.uniform(0, y_max, n_vis)
under = y_vis <= f(x_vis)

ax2.scatter(x_vis[under],  y_vis[under],  s=1, c="steelblue", alpha=0.5, label="Під кривою")
ax2.scatter(x_vis[~under], y_vis[~under], s=1, c="salmon",    alpha=0.3, label="Над кривою")
ax2.plot(x_plot[(x_plot >= a) & (x_plot <= b)],
         f(x_plot[(x_plot >= a) & (x_plot <= b)]), "r", linewidth=2)
ax2.set_xlim([a, b]); ax2.set_ylim([0, y_max])
ax2.set_xlabel("x"); ax2.set_ylabel("y")
ax2.set_title(f"Точки Монте-Карло (показано {n_vis:,})")
ax2.legend(markerscale=6); ax2.grid(alpha=0.4)

plt.tight_layout()
plt.savefig(".monte_carlo_plot.png", dpi=150)
plt.close()
print("Графік збережено.")