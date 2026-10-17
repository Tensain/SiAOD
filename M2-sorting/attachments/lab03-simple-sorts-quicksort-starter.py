#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 3. Простые сортировки и QuickSort с рандомизацией — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-03 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python lab03-simple-sorts-quicksort-starter.py --variant N
"""
from __future__ import annotations
from collections import defaultdict
import math
from pathlib import Path

import argparse
import random
import statistics
import time

# ---------------------------------------------------------------------------
# 1. Простые сортировки со счётчиками (сортируют КОПИЮ входа, вход не меняют)
#    Каждая функция возвращает кортеж: (отсортированный список,
#    число сравнений ключей, число обменов/перемещений элементов).
# ---------------------------------------------------------------------------


def bubble_sort(a: list) -> tuple[list, int, int]:
    """Сортировка пузырьком. Ожидаемая сложность: (обосновать в отчёте).

    Подсказка: досрочный выход, если за проход не было ни одного обмена, —
    именно он даёт лучший случай на упорядоченном входе.
    """
    # реализовать; считать сравнения и обмены

    to_sort = a[::]
    n = len(to_sort)
    comps = 0 # сколько сравнили
    swaps = 0 # сколько поменяли 

    for i in range(n - 1):
        swap = False
        for j in range(n - 1 - i):
            comps += 1
            if to_sort[j] > to_sort[j + 1]:
                to_sort[j], to_sort[j + 1] = to_sort[j + 1], to_sort[j]
                swaps += 1
                swap = True
        if not swap:
            break

    return (to_sort, comps, swaps)
    # raise NotImplementedError


def insertion_sort(a: list) -> tuple[list, int, int]:
    """Сортировка вставками. Ожидаемая сложность: TODO (лучший/худший случаи)."""
    # реализовать; считать сравнения и перемещения (сдвиги)

    to_sort = a[::]
    n = len(to_sort)
    comps = 0 # сколько сравнили
    swaps = 0 # сколько поменяли 

    for i in range(1, n):
        x = to_sort[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if to_sort[j] > x:
                swaps += 1
                to_sort[j + 1] = to_sort[j] # сдвиг
                j -= 1
            else:
                break
        to_sort[j + 1] = x

    return (to_sort, comps, swaps)
    # raise NotImplementedError


def selection_sort(a: list) -> tuple[list, int, int]:
    """Сортировка выбором. Ожидаемая сложность: TODO (почему не зависит от входа?)."""
    # реализовать; считать сравнения и обмены
    to_sort = a[::]
    n = len(to_sort)
    comps = 0 # сколько сравнили
    swaps = 0 # сколько поменяли 

    for i in range(n - 1):
        m = i # индекс минимума
        for j in range(i + 1, n):
            comps += 1
            if to_sort[j] < to_sort[m]:
                m = j
        to_sort[i], to_sort[m] = to_sort[m], to_sort[i]
        swaps += 1
    return (to_sort, comps, swaps)
    # raise NotImplementedError


# ---------------------------------------------------------------------------
# 2. QuickSort с рандомизированным опорным элементом
# ---------------------------------------------------------------------------


def quick_sort(a: list, rng: random.Random | None = None) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.

    Ожидаемая сложность: в среднем O(n log n), в худшем O(n²) (обосновать
    в отчёте, объяснить роль рандомизации). rng передаётся снаружи, чтобы
    запуск был воспроизводим по seed варианта.
    """
    if rng is None:
        rng = random.Random()
    to_sort = a[::]

    def partition(lo: int, hi: int) -> int:
        pivot_idx = rng.randrange(lo, hi)
        to_sort[pivot_idx], to_sort[hi - 1] = to_sort[hi - 1], to_sort[pivot_idx]
        pivot = to_sort[hi - 1]
        i = lo
        for j in range(lo, hi - 1):
            if to_sort[j] <= pivot:
                to_sort[i], to_sort[j] = to_sort[j], to_sort[i]
                i += 1
        to_sort[i], to_sort[hi - 1] = to_sort[hi - 1], to_sort[i]
        return i

    # Явный стек диапазонов [lo, hi) для обработки
    stack = [(0, len(to_sort))]
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        p = partition(lo, hi)
        # Сначала больший диапазон — чтобы стек рос логарифмически (O(log n) памяти)
        left_size = p - lo
        right_size = hi - p - 1
        if left_size < right_size:
            stack.append((p + 1, hi))
            stack.append((lo, p))
        else:
            stack.append((lo, p))
            stack.append((p + 1, hi))

    return to_sort
    # raise NotImplementedError


# ---------------------------------------------------------------------------
# 3. Демонстрация стабильности на парах (ключ, метка)
# ---------------------------------------------------------------------------


def stability_demo() -> None:
    """Показать, какие из четырёх сортировок стабильны.

    План: взять массив пар (ключ, метка) с повторяющимися ключами, например
    [(2, "a"), (1, "b"), (2, "c"), (1, "d")], отсортировать каждой сортировкой
    по ключу (сравнение только по p[0]!) и напечатать порядок меток при равных
    ключах. Вывод о стабильности каждой сортировки включить в отчёт.
    """
    # подготовить пары, прогнать все четыре сортировки, напечатать итог
    pairs = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]

    # Версии сортировок, сравнивающие только по ключу (первому элементу пары)
    def bubble_key(arr):
        to_sort = arr[::]
        n = len(to_sort)
        for i in range(n - 1):
            swapped = False
            for j in range(n - 1 - i):
                if to_sort[j][0] > to_sort[j + 1][0]:
                    to_sort[j], to_sort[j + 1] = to_sort[j + 1], to_sort[j]
                    swapped = True
            if not swapped:
                break
        return to_sort

    def insertion_key(arr):
        to_sort = arr[::]
        n = len(to_sort)
        for i in range(1, n):
            x = to_sort[i]
            j = i - 1
            while j >= 0 and to_sort[j][0] > x[0]:
                to_sort[j + 1] = to_sort[j]
                j -= 1
            to_sort[j + 1] = x
        return to_sort

    def selection_key(arr):
        to_sort = arr[::]
        n = len(to_sort)
        for i in range(n - 1):
            m = i
            for j in range(i + 1, n):
                if to_sort[j][0] < to_sort[m][0]:
                    m = j
            to_sort[i], to_sort[m] = to_sort[m], to_sort[i]
        return to_sort

    def quick_key(arr):
        rng = random.Random(42)  # фиксированный seed для воспроизводимости
        to_sort = arr[::]

        def partition(lo, hi):
            pivot_idx = rng.randrange(lo, hi)
            to_sort[pivot_idx], to_sort[hi - 1] = to_sort[hi - 1], to_sort[pivot_idx]
            pivot = to_sort[hi - 1][0]
            i = lo
            for j in range(lo, hi - 1):
                if to_sort[j][0] <= pivot:
                    to_sort[i], to_sort[j] = to_sort[j], to_sort[i]
                    i += 1
            to_sort[i], to_sort[hi - 1] = to_sort[hi - 1], to_sort[i]
            return i

        def qs(lo, hi):
            if lo >= hi:
                return
            p = partition(lo, hi)
            qs(lo, p)
            qs(p + 1, hi)

        qs(0, len(to_sort))
        return to_sort

    sorts = [
        ("bubble_sort", bubble_key),
        ("insertion_sort", insertion_key),
        ("selection_sort", selection_key),
        ("quick_sort", quick_key),
    ]

    print("\nДемонстрация стабильности на парах (ключ, метка):")
    print(f"  Исходный массив: {pairs}")
    print("  Ожидаемый порядок меток при стабильной сортировке:")
    print("    ключ 1: b, d (исходный порядок)")
    print("    ключ 2: a, c (исходный порядок)")
    print()

    for name, fn in sorts:
        result = fn(pairs)
        labels = [label for _, label in result]
        # Проверяем стабильность: для каждого ключа метки должны идти в исходном порядке
        key_order = defaultdict(list)
        for key, label in pairs:
            key_order[key].append(label)
        result_order = defaultdict(list)
        for key, label in result:
            result_order[key].append(label)
        stable = all(key_order[k] == result_order[k] for k in key_order)
        status = "СТАБИЛЬНА" if stable else "нестабильна"
        print(f"  {name:20s}: метки = {labels} — {status}")
    # raise NotImplementedError


# ---------------------------------------------------------------------------
# 4. Классы входов (данные по варианту, детерминированно по seed)
# ---------------------------------------------------------------------------


def make_inputs(n: int, seed: int) -> dict[str, list[int]]:
    """Три класса входов размера n: упорядоченный, случайный, обратный."""
    rng = random.Random(seed + n)  # свой поток для каждого размера
    data = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    return {
        "упорядоченный": sorted(data),
        "случайный": data,
        "обратный": sorted(data, reverse=True),
    }


# ---------------------------------------------------------------------------
# 5. Верификация (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------

ALGORITHMS = {
    "bubble_sort": lambda a: bubble_sort(a)[0],
    "insertion_sort": lambda a: insertion_sort(a)[0],
    "selection_sort": lambda a: selection_sort(a)[0],
    "quick_sort": lambda a: quick_sort(a, random.Random(0)),
}


def is_sorted(a: list) -> bool:
    """Инвариант 1: неубывающий порядок элементов."""
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def self_check() -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [5, 5, 5, 5],          # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for name, fn in ALGORITHMS.items():
        for a in boundary:
            res = fn(list(a))
            assert is_sorted(res), f"{name}: нарушен порядок на {a}"
            assert sorted(res) == sorted(a), f"{name}: не перестановка входа {a}"
    # Сверка с эталоном из стандартной библиотеки на сотнях случайных входов.
    rng = random.Random(0)
    for _ in range(300):
        a = [rng.randint(-100, 100) for _ in range(rng.randint(0, 80))]
        expected = sorted(a)
        for name, fn in ALGORITHMS.items():
            assert fn(list(a)) == expected, f"{name}: расходится с sorted() на {a}"

    # Счётчики: у сортировки выбором ровно n*(n-1)/2 сравнений на любом входе.
    _, comparisons, _ = selection_sort([3, 1, 2, 5, 4])
    assert comparisons == 10, "selection_sort: неверный счётчик сравнений"
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 6. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES_QUADRATIC = [500, 1_000, 2_000, 4_000, 8_000]     # для простых сортировок
SIZES_QUICK = [1_000, 3_000, 10_000, 30_000, 100_000]   # для QuickSort
REPEATS = 5


def bench(fn, data: list) -> float:
    """Медиана времени выполнения fn(копия data) по REPEATS запускам, с прогревом."""
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        arg = list(data)  # свежая копия: сортировка не должна получать свой результат
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)

def log_log_slope(points: list[tuple[int, float]]) -> float:
    """Наклон прямой в осях (log n, log t) — оценка показателя степени."""
    xs = [math.log10(n) for n, _ in points]
    ys = [math.log10(t) for _, t in points]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return (sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            / sum((x - mx) ** 2 for x in xs))

def run_benchmarks(seed: int) -> None:
    """Замеры всех алгоритмов на трёх классах входов; результат — таблица в stdout."""
    plans = [
        ("bubble_sort", ALGORITHMS["bubble_sort"], SIZES_QUADRATIC),
        ("insertion_sort", ALGORITHMS["insertion_sort"], SIZES_QUADRATIC),
        ("selection_sort", ALGORITHMS["selection_sort"], SIZES_QUADRATIC),
        ("quick_sort", lambda a: quick_sort(a, random.Random(seed)), SIZES_QUICK),
    ]
    plot_data: dict[str, dict[str, list[tuple[int, float]]]] = {}

    for name, fn, sizes in plans:
        print(f"\n{name}:")
        plot_data[name] = {}
        for cls in ["упорядоченный", "случайный", "обратный"]:
            points = []
            for n in sizes:
                data = make_inputs(n, seed)[cls]
                t = bench(fn, data)
                points.append((n, t))
                print(f"  n={n:>7}  вход={cls:<13} t={t:.6f} c")
            plot_data[name][cls] = points

    print("\nТаблицы счётчиков (на случайном входе n=1000):")
    n_demo = 1000
    rng_demo = random.Random(seed + n_demo)
    demo_data = [rng_demo.randint(-1000, 1000) for _ in range(n_demo)]
    for name, fn in [("bubble_sort", bubble_sort),
                     ("insertion_sort", insertion_sort),
                     ("selection_sort", selection_sort)]:
        _, comps, ops = fn(demo_data)
        op_name = "обменов" if name != "insertion_sort" else "сдвигов"
        print(f"  {name:20s}: сравнений = {comps:>7}, {op_name} = {ops:>7}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib не установлен — графики пропущены "
              "(pip install -r requirements.txt)")
        return

    # Цвета и маркеры для классов входов
    colors = {"упорядоченный": "green", "случайный": "blue", "обратный": "red"}
    markers = {"упорядоченный": "o", "случайный": "s", "обратный": "^"}

    # --- График 1: простые сортировки (log-log) ---
    fig, ax = plt.subplots(figsize=(10, 7))
    for name in ["bubble_sort", "insertion_sort", "selection_sort"]:
        for cls in ["упорядоченный", "случайный", "обратный"]:
            points = plot_data[name][cls]
            ns = [n for n, _ in points]
            ts = [t for _, t in points]
            slope = log_log_slope(points) if len(points) >= 2 else 0.0
            ax.plot(ns, ts,
                    marker=markers[cls], color=colors[cls],
                    label=f"{name} ({cls}, наклон≈{slope:.2f})",
                    alpha=0.7, linewidth=1.5)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("размер входа n")
    ax.set_ylabel("время, с")
    ax.set_title("Простые сортировки: время работы в осях log-log")
    ax.grid(True, which="both", linewidth=0.3)
    ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(Path.cwd() / "lab03_sorts.png", dpi=150)
    print("\nГрафик сохранён: lab03_sorts.png")

    # --- График 2: QuickSort (log-log) с референсом O(n log n) ---
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    for cls in ["упорядоченный", "случайный", "обратный"]:
        points = plot_data["quick_sort"][cls]
        ns = [n for n, _ in points]
        ts = [t for _, t in points]
        slope = log_log_slope(points) if len(points) >= 2 else 0.0
        ax2.plot(ns, ts,
                 marker=markers[cls], color=colors[cls],
                 label=f"quick_sort ({cls}, наклон≈{slope:.2f})")
    # Референсная линия O(n log n) для сопоставления
    import math
    ref_ns = SIZES_QUICK
    # Масштабируем референс, чтобы он был виден рядом с замерами
    ref_ts = [n * math.log2(n) * 1e-9 for n in ref_ns]
    ax2.plot(ref_ns, ref_ts, "k--", label="O(n log n) (референс)", linewidth=1)
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("размер входа n")
    ax2.set_ylabel("время, с")
    ax2.set_title("QuickSort: время работы в осях log-log")
    ax2.grid(True, which="both", linewidth=0.3)
    ax2.legend(fontsize=9)
    fig2.tight_layout()
    fig2.savefig(Path.cwd() / "lab03_quicksort.png", dpi=150)
    print("График сохранён: lab03_quicksort.png")
    # TODO: построить log-log графики (matplotlib) по классам входов;
    # TODO: сопоставить наклоны с O(n^2) и O(n log n), объяснить расхождения
    #       (в т. ч. лучший случай вставок и поведение пузырька на упорядоченном входе);
    # TODO: включить в отчёт таблицы счётчиков сравнений/обменов.


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    stability_demo()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
