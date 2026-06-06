import os
import re
import matplotlib.pyplot as plt
import pandas as pd

# Список файлів для обробки
file_names = ["results1.txt", "results2.txt", "results3.txt", "results4.txt"]
data_list = []


def parse_file_content(content, run_idx):
    file_data = []

    # Надійно ділимо текст за ключовим словом Article (ігноруючи пробіли навколо)
    articles = re.split(r"Article\s+", content)

    for art_block in articles[1:]:  # Пропускаємо текст до першої статті
        # Витягуємо номер статті
        art_match = re.match(r"^(\d+)", art_block)
        if not art_match:
            continue
        art_num = f"Article {art_match.group(1)}"

        # Ділимо статтю на окремі патерни
        patterns = re.split(r"Pattern\s+", art_block)
        for patt_block in patterns[1:]:
            # Шукаємо номер патерна та його тип (existing або fake)
            patt_match = re.match(r"^(\d+)\s*\((existing|fake)\)", patt_block)
            if not patt_match:
                continue
            patt_type = patt_match.group(2)

            # Шукаємо час виконання для кожного з трьох алгоритмів
            bm_match = re.search(r"Boyer-Moore:\s*([\d.]+)", patt_block)
            kmp_match = re.search(
                r"Knuth-Morris-Pratt:\s*([\d.]+)", patt_block
            )
            rk_match = re.search(r"Rabin-Karp:\s*([\d.]+)", patt_block)

            # Додаємо дані, якщо алгоритми знайдено
            if bm_match:
                file_data.append(
                    {
                        "Run": run_idx,
                        "Article": art_num,
                        "Pattern Type": patt_type,
                        "Algorithm": "Boyer-Moore",
                        "Time (µs)": float(bm_match.group(1)),
                    }
                )
            if kmp_match:
                file_data.append(
                    {
                        "Run": run_idx,
                        "Article": art_num,
                        "Pattern Type": patt_type,
                        "Algorithm": "Knuth-Morris-Pratt",
                        "Time (µs)": float(kmp_match.group(1)),
                    }
                )
            if rk_match:
                file_data.append(
                    {
                        "Run": run_idx,
                        "Article": art_num,
                        "Pattern Type": patt_type,
                        "Algorithm": "Rabin-Karp",
                        "Time (µs)": float(rk_match.group(1)),
                    }
                )

    return file_data


# Зчитуємо та парсимо кожен файл
for idx, file_name in enumerate(file_names, start=1):
    if not os.path.exists(file_name):
        print(f"Попередження: Файл {file_name} не знайдено.")
        continue

    with open(file_name, "r", encoding="utf-8") as f:
        file_content = f.read()
        parsed_entries = parse_file_content(file_content, idx)
        data_list.extend(parsed_entries)

# Перевірка на випадок, якщо дані взагалі не зчиталися
if not data_list:
    raise ValueError(
        "Не вдалося зчитати дані з файлів. Перевірте шляхи до файлів та їх вміст."
    )

# Створюємо DataFrame
df = pd.DataFrame(data_list)

# 1. ПОБУДОВА ТАБЛИЦЬ РЕЗУЛЬТАТІВ
print("=== ЗВЕДЕНА ТАБЛИЦЯ ЧАСУ ВИКОНАННЯ (µs) ===")
pivot_df = df.pivot_table(
    index=["Article", "Pattern Type", "Algorithm"],
    columns="Run",
    values="Time (µs)",
)
print(pivot_df)
print("\n" + "=" * 60 + "\n")


# 2. ПОБУДОВА ГРАФІКІВ
# Налаштування кольорів (темніший для existing, яскравіший/світліший для fake)
colors = {
    ("Boyer-Moore", "existing"): "#004080",  # Темно-синій
    ("Boyer-Moore", "fake"): "#66b2ff",  # Світло-синій
    ("Knuth-Morris-Pratt", "existing"): "#008217",  # Темно-зелений
    ("Knuth-Morris-Pratt", "fake"): "#5DE875",  # Яскраво-зелений
    ("Rabin-Karp", "existing"): "#990000",  # Темно-червоний
    ("Rabin-Karp", "fake"): "#ff6666",  # Світло-червоний
}

articles_unique = sorted(df["Article"].unique())

# Створюємо субграфіки для кожної статті окремо (бо тексти мають різну довжину)
fig, axes = plt.subplots(
    len(articles_unique), 1, figsize=(11, 5 * len(articles_unique)), sharex=True
)

if len(articles_unique) == 1:
    axes = [axes]

for ax, article in zip(axes, articles_unique):
    ax.set_title(
        f"Порівняння швидкодії алгоритмів для {article}", fontsize=14, pad=12
    )

    for (algo, patt_type), color in colors.items():
        # Відбираємо дані для конкретної статті, алгоритму та типу підрядка
        subset = df[
            (df["Article"] == article)
            & (df["Algorithm"] == algo)
            & (df["Pattern Type"] == patt_type)
        ].sort_values("Run")

        if not subset.empty:
            label = f"{algo} ({patt_type})"
            ax.plot(
                subset["Run"],
                subset["Time (µs)"],
                marker="o",
                markersize=6,
                linewidth=2,
                color=color,
                label=label,
            )

    ax.set_ylabel("Час виконання (µs)", fontsize=12)
    ax.set_xticks(df["Run"].unique())
    ax.grid(True, linestyle="--", alpha=0.5)
    # Розміщуємо легенду праворуч від графіку, щоб вона не перекривала лінії
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0.0)

axes[-1].set_xlabel("Номер запуску (Run)", fontsize=12)

plt.tight_layout()
# Зберігаємо графік у файл
plt.savefig("algorithm_performance_comparison.png", dpi=300)
print(
    "Графік успішно побудовано та збережено під назвою 'algorithm_performance_comparison.png'."
)
plt.show()