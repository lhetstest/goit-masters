import timeit
import os

# ─────────────────────────────────────────────
#  1.  ALGORITHM IMPLEMENTATIONS
# ─────────────────────────────────────────────

# ── Boyer-Moore ──────────────────────────────
def build_bad_char_table(pattern):
    table = {}
    for i, ch in enumerate(pattern):
        table[ch] = i
    return table

def boyer_moore(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    bad_char = build_bad_char_table(pattern)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s          # found
        shift = j - bad_char.get(text[s + j], -1)
        s += max(1, shift)
    return -1                 # not found


# ── Knuth-Morris-Pratt ───────────────────────
def build_kmp_failure(pattern):
    m = len(pattern)
    failure = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = failure[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        failure[i] = k
    return failure

def kmp(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    failure = build_kmp_failure(pattern)
    k = 0
    for i in range(n):
        while k > 0 and pattern[k] != text[i]:
            k = failure[k - 1]
        if pattern[k] == text[i]:
            k += 1
        if k == m:
            return i - m + 1  # found
    return -1                  # not found


# ── Rabin-Karp ───────────────────────────────
def rabin_karp(text, pattern, base=256, mod=101):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    h = pow(base, m - 1, mod)
    p_hash = t_hash = 0
    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % mod
        t_hash = (base * t_hash + ord(text[i])) % mod
    for s in range(n - m + 1):
        if p_hash == t_hash:
            if text[s:s + m] == pattern:
                return s      # found
        if s < n - m:
            t_hash = (base * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % mod
            if t_hash < 0:
                t_hash += mod
    return -1                  # not found


# ─────────────────────────────────────────────
#  2.  TIMING HELPER
# ─────────────────────────────────────────────
TIMEIT_NUMBER = 1000   # repetitions per measurement

def measure(func, text, pattern):
    timer = timeit.Timer(lambda: func(text, pattern))
    total = timer.timeit(number=TIMEIT_NUMBER)
    return total / TIMEIT_NUMBER   # average per call (seconds)


# ─────────────────────────────────────────────
#  3.  LOAD ARTICLES  (put article1.txt / article2.txt
#      next to this script, or edit the paths below)
# ─────────────────────────────────────────────
ARTICLE1_PATH = "./text1.txt"
ARTICLE2_PATH = "./text2.txt"

def load_text(path):
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"File '{path}' not found.\n"
            "Please save your article files as text1.txt and text2.txt "
            "in the same folder as this script."
        )
    with open(path, encoding="utf-8") as f:
        return f.read()


# ─────────────────────────────────────────────
#  4.  PATTERNS
# ─────────────────────────────────────────────
patterns = {
    "article1": {
        "existing": "структури даних",
        "fake":     "Кувала зозуля",
    },
    "article2": {
        "existing": "аргументи функції",
        "fake":     "Кувала зозуля",
    },
}

algorithms = [
    ("Boyer-Moore",        boyer_moore),
    ("Knuth-Morris-Pratt", kmp),
    ("Rabin-Karp",         rabin_karp),
]


# ─────────────────────────────────────────────
#  5.  RUN COMPARISONS
# ─────────────────────────────────────────────
def run_comparison(article_key, text, results_store):
    pat_existing = patterns[article_key]["existing"]
    pat_fake     = patterns[article_key]["fake"]

    print(f"\n{'─'*55}")
    print(f"  {article_key.upper()}  (length = {len(text)})")
    print(f"{'─'*55}")

    data = {"length": len(text), "patterns": {}}

    for label, pattern in [("existing", pat_existing), ("fake", pat_fake)]:
        print(f"\n  Pattern ({label}): '{pattern}'")
        # quick sanity check
        found_bm = boyer_moore(text, pattern)
        status = f"found at index {found_bm}" if found_bm != -1 else "NOT FOUND"
        print(f"  → {status}")
        print()

        data["patterns"][label] = {"pattern": pattern, "times": {}}

        for name, func in algorithms:
            t = measure(func, text, pattern)
            data["patterns"][label]["times"][name] = t
            print(f"    {name:<25} {t*1e6:>10.4f} µs")

    results_store[article_key] = data


# ─────────────────────────────────────────────
#  6.  WRITE RESULTS FILE + CONCLUSIONS
# ─────────────────────────────────────────────
def fmt_time(seconds):
    µs = seconds * 1_000_000
    return f"{µs:.4f} µs"

def write_results(results, output_path="results.txt"):
    lines = []

    overall_times = {name: 0.0 for name, _ in algorithms}

    for art_idx, (art_key, art_label) in enumerate(
            [("article1", "Article 1"), ("article2", "Article 2")], start=1):
        data = results[art_key]
        lines.append(f"{art_label} (length = {data['length']})")

        fastest_per_article = {}

        for pat_key, pat_label in [("existing", "Pattern 1 (existing): "),
                                    ("fake",     "Pattern 2 (fake): ")]:
            lines.append(f"  {pat_label}")
            lines.append(f"  Pattern: \"{data['patterns'][pat_key]['pattern']}\"")
            times = data["patterns"][pat_key]["times"]
            for name, _ in algorithms:
                t = times[name]
                lines.append(f"  {name}: {fmt_time(t)}")
                overall_times[name] += t
            # fastest for this pattern
            best = min(times, key=times.get)
            lines.append(f"  → Fastest: {best}")
            fastest_per_article[pat_key] = best
            lines.append("")

        # fastest for this article overall (sum of both patterns)
        art_totals = {}
        for name, _ in algorithms:
            art_totals[name] = (
                data["patterns"]["existing"]["times"][name] +
                data["patterns"]["fake"]["times"][name]
            )
        best_art = min(art_totals, key=art_totals.get)
        lines.append(f"  ★ Fastest algorithm for {art_label}: {best_art}")
        lines.append("")
        lines.append("─" * 55)
        lines.append("")

    # ── Overall conclusion ──
    best_overall = min(overall_times, key=overall_times.get)
    lines.append("═" * 55)
    lines.append("OVERALL SUMMARY")
    lines.append("═" * 55)
    lines.append("")
    lines.append("Cumulative average time across all tests:")
    for name, _ in algorithms:
        lines.append(f"  {name:<25} {fmt_time(overall_times[name])}")
    lines.append("")
    lines.append(f"★ BEST OVERALL ALGORITHM: {best_overall}")
    lines.append("")
    lines.append("─" * 55)

    text_out = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text_out)
    print(f"\n✔  Результати збережено в '{output_path}'")
    return text_out


# ─────────────────────────────────────────────
#  7.  MAIN
# ─────────────────────────────────────────────
def main():
    print("Loading articles …")
    article1 = load_text(ARTICLE1_PATH)
    article2 = load_text(ARTICLE2_PATH)

    results = {}
    run_comparison("article1", article1, results)
    run_comparison("article2", article2, results)

    output = write_results(results, output_path="results.txt")
    print("\n" + "═"*55)
    print("RESULTS FILE PREVIEW")
    print("═"*55)
    print(output)


if __name__ == "__main__":
    main()
