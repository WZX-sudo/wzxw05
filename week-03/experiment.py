"""蒲丰投针：用随机投针估计圆周率，并把真实参数与结果写入 results.csv。

只依赖标准库；import 本模块不会启动实验，也不会写任何文件。
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path

FIELDS = ("seed", "n", "crossings", "pi_estimate", "needle_length", "line_spacing")
DEFAULT_SEED = 42
DEFAULT_LENGTH = 0.5
DEFAULT_SPACING = 1.0
DEFAULT_SIZES = (1000, 10000, 100000)


def _check_geometry(length: float, spacing: float) -> None:
    """本实验只定义 0 < length <= spacing 的几何，不静默改动参数。"""
    if not math.isfinite(length) or not math.isfinite(spacing):
        raise ValueError(f"length 和 spacing 必须是有限数，收到 length={length}, spacing={spacing}")
    if not 0 < length <= spacing:
        raise ValueError(f"要求 0 < length <= spacing，收到 length={length}, spacing={spacing}")


def _require_int(value: object, name: str) -> int:
    """计数必须是真正的整数；bool 虽然是 int 的子类，但不算计数。"""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} 必须是整数，收到 {value!r}")
    return value


def crosses_line(distance: float, angle: float, length: float = 0.5, spacing: float = 1.0) -> bool:
    """判断一根针是否与某条平行线相交；针尖恰好触线也算相交。

    distance 是针的中心到最近一条线的距离，angle 是针与平行线的夹角（弧度）。
    """
    _check_geometry(length, spacing)
    if not math.isfinite(distance) or not 0 <= distance <= spacing / 2:
        raise ValueError(f"distance 必须在 [0, spacing/2] 内，收到 {distance}")
    if not math.isfinite(angle) or not 0 <= angle <= math.pi / 2:
        raise ValueError(f"angle 必须在 [0, pi/2] 内，收到 {angle}")
    # 半根针沿垂直方向的伸出距离；相等时算触线。
    return distance <= length / 2 * math.sin(angle)


def estimate_pi(n: int, crossings: int, length: float = 0.5, spacing: float = 1.0) -> float:
    """由投针数与相交数估计圆周率：2 * length * n / (spacing * crossings)。"""
    _check_geometry(length, spacing)
    n = _require_int(n, "n")
    if n <= 0:
        raise ValueError(f"n 必须是正整数，收到 {n}")
    crossings = _require_int(crossings, "crossings")
    if crossings == 0:
        raise ValueError("crossings=0 时 2*length*n/(spacing*crossings) 无定义，无法估计圆周率")
    if not 0 < crossings <= n:
        raise ValueError(f"crossings 必须满足 0 < crossings <= n，收到 crossings={crossings}, n={n}")
    return 2 * length * n / (spacing * crossings)


def simulate(n: int, seed: int = 42, length: float = 0.5, spacing: float = 1.0) -> dict:
    """独立投 n 根针，返回本次实验的真实参数、相交数与估计值。"""
    _check_geometry(length, spacing)
    n = _require_int(n, "n")
    if n <= 0:
        raise ValueError(f"n 必须是正整数，收到 {n}")
    # 每次独立实验只初始化一次生成器，循环内不再重设 seed。
    rng = random.Random(seed)
    crossings = 0
    for _ in range(n):
        distance = rng.uniform(0.0, spacing / 2)
        angle = rng.uniform(0.0, math.pi / 2)
        crossings += crosses_line(distance, angle, length, spacing)
    if crossings == 0:
        raise ValueError(f"这次 n={n} 的投针没有任何相交，无法给出估计值")
    return {
        "seed": seed,
        "n": n,
        "crossings": crossings,
        "pi_estimate": estimate_pi(n, crossings, length, spacing),
        "needle_length": length,
        "line_spacing": spacing,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="蒲丰投针：估计圆周率并写出 results.csv")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="每组实验开始时初始化一次")
    parser.add_argument("--n", type=int, nargs="+", default=list(DEFAULT_SIZES), help="投针次数，可给多组")
    parser.add_argument("--length", type=float, default=DEFAULT_LENGTH, help="针的全长")
    parser.add_argument("--spacing", type=float, default=DEFAULT_SPACING, help="相邻平行线的间距")
    args = parser.parse_args(argv)

    output = Path.cwd() / "results.csv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for n in args.n:
            row = simulate(n, seed=args.seed, length=args.length, spacing=args.spacing)
            writer.writerow(row)
            print(
                f"seed={row['seed']}, n={row['n']}, crossings={row['crossings']}, "
                f"pi_estimate={row['pi_estimate']:.8f}"
            )
    print(f"wrote {output.name} ({len(args.n)} runs)")


if __name__ == "__main__":
    main()
