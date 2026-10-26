"""Lab 3: Smart Resource Allocation and Scheduling System using Greedy Algorithms
Modules: Fractional Knapsack, Activity Selection, Huffman Coding + performance + plots
"""
import heapq
import random
import string
import time
import tracemalloc
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------------- Q2: Fractional Knapsack ----------------
def fractional_knapsack(items, capacity):
    sorted_items = sorted(items, key=lambda x: x["value"] / x["weight"], reverse=True)
    total_value, chosen, remaining = 0.0, [], capacity
    for item in sorted_items:
        if remaining <= 0:
            break
        if item["weight"] <= remaining:
            total_value += item["value"]
            remaining -= item["weight"]
            chosen.append((item["name"], 1.0))
        else:
            fraction = remaining / item["weight"]
            total_value += item["value"] * fraction
            chosen.append((item["name"], fraction))
            remaining = 0
    return total_value, chosen


# ---------------- Q3: Activity Selection ----------------
def activity_selection(activities):
    sorted_acts = sorted(activities, key=lambda a: a["finish"])
    selected = [sorted_acts[0]]
    last_finish = sorted_acts[0]["finish"]
    for act in sorted_acts[1:]:
        if act["start"] >= last_finish:
            selected.append(act)
            last_finish = act["finish"]
    return selected


# ---------------- Q4: Huffman Coding ----------------
class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char, self.freq, self.left, self.right = char, freq, left, right

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    frequency = Counter(text)
    heap = [Node(ch, f) for ch, f in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, Node(None, left.freq + right.freq, left, right))
    return heap[0]


def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node is None:
        return codebook
    if node.char is not None:
        codebook[node.char] = prefix or "0"
        return codebook
    generate_codes(node.left, prefix + "0", codebook)
    generate_codes(node.right, prefix + "1", codebook)
    return codebook


def huffman_encode(text):
    root = build_huffman_tree(text)
    codebook = generate_codes(root)
    encoded = "".join(codebook[ch] for ch in text)
    return encoded, codebook


# ---------------- Q6: Visualizations ----------------
def plot_knapsack_allocation(selection, path):
    names = [s[0] for s in selection]
    fractions = [s[1] * 100 for s in selection]
    plt.figure(figsize=(7, 4))
    bars = plt.bar(names, fractions, color="#4472C4")
    for b, f in zip(bars, fractions):
        plt.text(b.get_x() + b.get_width() / 2, f + 1, f"{f:.1f}%", ha="center")
    plt.ylabel("Percentage of Item Taken (%)")
    plt.ylim(0, 115)
    plt.title("Fractional Knapsack - Resource Allocation")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def plot_activity_timeline(all_acts, selected, path):
    sel_names = {a["name"] for a in selected}
    acts = sorted(all_acts, key=lambda a: a["start"])
    plt.figure(figsize=(8, 4.5))
    for i, act in enumerate(acts):
        chosen = act["name"] in sel_names
        plt.barh(i, act["finish"] - act["start"], left=act["start"],
                 color="#70AD47" if chosen else "#BFBFBF", edgecolor="black")
        plt.text(act["start"] + (act["finish"] - act["start"]) / 2, i, act["name"],
                 va="center", ha="center", fontsize=9)
    plt.xlabel("Time")
    plt.yticks([])
    plt.title("Activity Selection - Timeline (green = selected, grey = rejected)")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def _layout(node, depth, x, pos):
    """Assign (x, y) positions with in-order x so the tree does not overlap."""
    if node is None:
        return x
    x = _layout(node.left, depth + 1, x, pos)
    pos[id(node)] = (x, -depth)
    x += 1
    x = _layout(node.right, depth + 1, x, pos)
    return x


def plot_huffman_tree(root, path):
    pos = {}
    _layout(root, 0, 0, pos)
    plt.figure(figsize=(9, 5))

    def draw(node):
        if node is None:
            return
        x, y = pos[id(node)]
        for child, bit in ((node.left, "0"), (node.right, "1")):
            if child is not None:
                cx, cy = pos[id(child)]
                plt.plot([x, cx], [y, cy], color="gray", zorder=1)
                plt.text((x + cx) / 2, (y + cy) / 2 + 0.08, bit, color="red",
                         fontsize=10, ha="center", fontweight="bold")
                draw(child)
        label = f"{node.char}\n{node.freq}" if node.char is not None else str(node.freq)
        color = "#A9D18E" if node.char is not None else "#9DC3E6"
        plt.scatter([x], [y], s=900, color=color, edgecolor="black", zorder=2)
        plt.text(x, y, label, ha="center", va="center", fontsize=8, zorder=3)

    draw(root)
    plt.axis("off")
    plt.title("Huffman Tree for 'abracadabra' (0 = left, 1 = right)")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


# ---------------- Q5: Performance measurement ----------------
def measure(func, *args, repeats=5):
    best = float("inf")
    for _ in range(repeats):
        t = time.perf_counter()
        func(*args)
        best = min(best, time.perf_counter() - t)
    tracemalloc.start()
    func(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return best, peak / 1024  # seconds, KB


def gen_items(n):
    return [{"name": f"I{i}", "weight": random.randint(1, 100),
             "value": random.randint(1, 500)} for i in range(n)]


def gen_acts(n):
    out = []
    for i in range(n):
        s = random.randint(0, n * 5)
        out.append({"name": f"A{i}", "start": s, "finish": s + random.randint(1, 20)})
    return out


def gen_text(n):
    return "".join(random.choices(string.ascii_lowercase, k=n))


def run_experiments(sizes):
    random.seed(7)
    rows = []
    for n in sizes:
        items, acts, text = gen_items(n), gen_acts(n), gen_text(n)
        cap = sum(i["weight"] for i in items) // 2
        tk, mk = measure(fractional_knapsack, items, cap)
        ta, ma = measure(activity_selection, acts)
        th, mh = measure(huffman_encode, text)
        rows.append({"n": n, "knap_t": tk, "knap_m": mk, "act_t": ta, "act_m": ma,
                     "huf_t": th, "huf_m": mh})
    return rows


def plot_performance(rows, time_path, mem_path):
    ns = [r["n"] for r in rows]
    plt.figure(figsize=(7.5, 4.5))
    plt.plot(ns, [r["knap_t"] * 1000 for r in rows], marker="o", label="Fractional Knapsack")
    plt.plot(ns, [r["act_t"] * 1000 for r in rows], marker="s", label="Activity Selection")
    plt.plot(ns, [r["huf_t"] * 1000 for r in rows], marker="^", label="Huffman Coding")
    plt.xlabel("Input size (n)")
    plt.ylabel("Execution time (ms)")
    plt.title("Execution Time vs Input Size")
    plt.grid(True, alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(time_path, dpi=150)
    plt.close()

    plt.figure(figsize=(7.5, 4.5))
    plt.plot(ns, [r["knap_m"] for r in rows], marker="o", label="Fractional Knapsack")
    plt.plot(ns, [r["act_m"] for r in rows], marker="s", label="Activity Selection")
    plt.plot(ns, [r["huf_m"] for r in rows], marker="^", label="Huffman Coding")
    plt.xlabel("Input size (n)")
    plt.ylabel("Peak memory (KB)")
    plt.title("Peak Memory Usage vs Input Size")
    plt.grid(True, alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(mem_path, dpi=150)
    plt.close()


if __name__ == "__main__":
    import json
    out = "."   # charts and results.json are saved in the current folder
    results = {}

    # Q2
    items = [{"name": "Gold", "weight": 10, "value": 60},
             {"name": "Silver", "weight": 20, "value": 100},
             {"name": "Bronze", "weight": 30, "value": 120}]
    value, selection = fractional_knapsack(items, 50)
    print("Maximum achievable value:", value)
    for name, frac in selection:
        print(f"  {name}: {frac * 100:.1f}% taken")
    results["knap"] = {"value": value, "sel": selection}
    plot_knapsack_allocation(selection, f"{out}/knapsack_allocation.png")

    # Q3
    activities = [{"name": "A1", "start": 1, "finish": 4}, {"name": "A2", "start": 3, "finish": 5},
                  {"name": "A3", "start": 0, "finish": 6}, {"name": "A4", "start": 5, "finish": 7},
                  {"name": "A5", "start": 3, "finish": 9}, {"name": "A6", "start": 5, "finish": 9},
                  {"name": "A7", "start": 6, "finish": 10}, {"name": "A8", "start": 8, "finish": 11}]
    result = activity_selection(activities)
    print("Selected activities:")
    for a in result:
        print(f"  {a['name']}: [{a['start']}, {a['finish']}]")
    results["act"] = [(a["name"], a["start"], a["finish"]) for a in result]
    plot_activity_timeline(activities, result, f"{out}/activity_timeline.png")

    # Q4
    text = "abracadabra"
    encoded, codebook = huffman_encode(text)
    print("Huffman codes:", codebook)
    print("Encoded bits :", encoded)
    ob = len(text) * 8
    print(f"Original size: {ob} bits, Compressed size: {len(encoded)} bits")
    print(f"Compression ratio: {len(encoded) / ob:.2%}")
    results["huf"] = {"codes": codebook, "encoded": encoded, "orig": ob, "comp": len(encoded)}
    plot_huffman_tree(build_huffman_tree(text), f"{out}/huffman_tree.png")

    # Q5 / Q6 performance
    rows = run_experiments([100, 500, 1000, 5000, 10000, 20000, 50000])
    print("\n n | knap ms/KB | act ms/KB | huffman ms/KB")
    for r in rows:
        print(f"{r['n']:>6} | {r['knap_t']*1000:.3f}/{r['knap_m']:.1f} | "
              f"{r['act_t']*1000:.3f}/{r['act_m']:.1f} | {r['huf_t']*1000:.3f}/{r['huf_m']:.1f}")
    results["rows"] = rows
    plot_performance(rows, f"{out}/performance_time.png", f"{out}/performance_memory.png")
    json.dump(results, open(f"{out}/results.json", "w"), indent=1)
