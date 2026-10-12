"""读取真实的 results.csv，生成报告需要的表格、参数说明和静态图。

这一步不重新投针、不编造结果：所有数字都来自当前目录的 CSV。
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_NAME = "results.csv"
TABLE_NAME = "results-table.tex"
PARAMS_NAME = "results-params.tex"
FIGURE_NAME = "results.png"
FIELDS_EXPECTED = ("seed", "n", "crossings", "pi_estimate", "needle_length", "line_spacing")


def load_rows(root: Path) -> list[dict[str, str]]:
    """读入 CSV 并检查表头，避免把不完整的结果画进报告。"""
    with (root / CSV_NAME).open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(FIELDS_EXPECTED):
            raise ValueError(f"{CSV_NAME} 的表头是 {reader.fieldnames}，与实验输出不一致")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{CSV_NAME} 里没有任何实验结果")
    return rows


def write_table(root: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        r"\begin{tabular}{rrr}",
        r"\toprule",
        r"$N$ & $K$ & $\widehat{\pi}$ \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{int(row['n'])} & {int(row['crossings'])} & {float(row['pi_estimate']):.6f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    (root / TABLE_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_params(root: Path, rows: list[dict[str, str]]) -> None:
    """写成可直接 \\input 的普通段落，数字全部取自本份 CSV。"""
    seeds = ", ".join(str(value) for value in sorted({int(row["seed"]) for row in rows}))
    sizes = ", ".join(str(int(row["n"])) for row in rows)
    lengths = ", ".join(sorted({row["needle_length"] for row in rows}, key=float))
    spacings = ", ".join(sorted({row["line_spacing"] for row in rows}, key=float))
    text = f"本次实际参数：seed = {seeds}；$N$ = {sizes}；针长 $L$ = {lengths}；平行线间距 $d$ = {spacings}。\n"
    (root / PARAMS_NAME).write_text(text, encoding="utf-8")


def write_figure(root: Path, rows: list[dict[str, str]]) -> None:
    sizes = [int(row["n"]) for row in rows]
    estimates = [float(row["pi_estimate"]) for row in rows]
    figure, axes = plt.subplots(figsize=(7.0, 3.2), constrained_layout=True)
    axes.plot(sizes, estimates, marker="o", label=r"Buffon estimate $\widehat{\pi}$")
    axes.axhline(math.pi, color="black", linestyle="--", linewidth=1.0, label=r"true $\pi$")
    axes.set_xscale("log")
    axes.set_xlabel("Number of needles (N)")
    axes.set_ylabel(r"Estimated $\pi$")
    axes.grid(alpha=0.25)
    axes.legend()
    figure.savefig(root / FIGURE_NAME, dpi=180)
    plt.close(figure)


def main() -> None:
    root = Path.cwd()
    rows = load_rows(root)
    write_table(root, rows)
    write_params(root, rows)
    write_figure(root, rows)
    print(f"wrote {TABLE_NAME}, {PARAMS_NAME} and {FIGURE_NAME} from {CSV_NAME}")


if __name__ == "__main__":
    main()
