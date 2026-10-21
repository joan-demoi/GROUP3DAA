import sys
import time
import math

# ==============================================================================
# PART 1: IMPLEMENTATION, CALL COUNTERS & BASE EQUIVALENCE VERIFICATION
# Scope: Implement Algorithm A (plain recursion) and Algorithm B (memoized), 
# global call counters, and verify equivalence for n = 0 to 20.
# ==============================================================================

calls_a = 0
calls_b = 0
fibtable = {}

def fib_a(n):
    """Algorithm A: Plain Recursion with global call counter."""
    global calls_a
    calls_a += 1
    if n == 0 or n == 1:
        return n
    return fib_a(n - 1) + fib_a(n - 2)


def fib_b(n):
    """Algorithm B: Memoized Recursion with global call counter."""
    global calls_b
    calls_b += 1
    
    # Explicit membership check avoids falsy zero evaluation bug
    if n in fibtable:
        return fibtable[n]
    
    if n == 0 or n == 1:
        value = n
    else:
        value = fib_b(n - 1) + fib_b(n - 2)
        
    fibtable[n] = value
    return value


def verify_base_equivalence():
    """Checks that both functions return identical values for n = 0 to 20."""
    global fibtable, calls_a, calls_b
    for n in range(21):
        fibtable.clear()
        calls_a = 0
        calls_b = 0
        assert fib_a(n) == fib_b(n), f"Mismatch at n={n}"
    print("Part 1 Verified: Both algorithms match for n = 0 to 20.\n")


# ==============================================================================
# PART 2: EXPERIMENTS, BENCHMARKING & PLOTTING
# Scope: Measure execution time and call counts, print results table, 
# and generate visual representation using built-in libraries.
# ==============================================================================

def run_experiments():
    global calls_a, calls_b, fibtable
    print("--- PART 2: EXPERIMENTAL BENCHMARKS ---")
    
    # Algorithm A Benchmarks (stop if execution exceeds 60 seconds)
    print("Algorithm A Results:")
    print(f"{'n':<6} | {'Calls':<12} | {'Time (s)':<12}")
    print("-" * 35)
    results_a = []
    for n in [5, 10, 15, 20, 25, 30, 35]:
        calls_a = 0
        start = time.perf_counter()
        fib_a(n)
        elapsed = time.perf_counter() - start
        results_a.append({'n': n, 'calls': calls_a, 'time': elapsed})
        print(f"{n:<6} | {calls_a:<12,d} | {elapsed:<12.6f}")
        if elapsed > 60.0:
            break

    # Algorithm B Benchmarks (clear table before each run, adjust recursion limit)
    sys.setrecursionlimit(3000)
    print("\nAlgorithm B Results:")
    print(f"{'n':<6} | {'Calls':<12} | {'Time (s)':<12}")
    print("-" * 35)
    results_b = []
    for n in [10, 50, 100, 200, 500, 1000]:
        fibtable.clear()
        calls_b = 0
        start = time.perf_counter()
        fib_b(n)
        elapsed = time.perf_counter() - start
        results_b.append({'n': n, 'calls': calls_b, 'time': elapsed})
        print(f"{n:<6} | {calls_b:<12,d} | {elapsed:<12.6f}")

    return results_a, results_b


def plot_results(results_a, results_b):
    """Generates a graphical visualizer using built-in tkinter canvas."""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("CSC2107 Assignment 5.1 - Fibonacci Performance Plot")
        root.geometry("600\u00d7400" if "600\u00d7400" else "600x400")
        
        canvas = tk.Canvas(root, width=580, height=360, bg="white")
        canvas.pack(arg for arg in () if arg) or canvas.pack(padx=10, pady=10)
        
        canvas.create_text(300, 20, text="Algorithm A (Exponential Calls - Log Scale Representation)", font=("Arial", 10, "bold"), fill="red")
        canvas.create_text(300, 200, text="Algorithm B (Linear Calls - Memoized)", font=("Arial", 10, "bold"), fill="blue")
        
        # Draw simple representation bars
        for i, r in enumerate(results_a):
            x = 40 + i * 70
            h = min(120, int(math.log10(max(1, r['calls'])) * 20))
            canvas.create_rectangle(x, 170 - h, x + 40, 170, fill="red")
            canvas.create_text(x + 20, 185, text=f"n={r['n']}")
            
        for i, r in enumerate(results_b):
            x = 40 + i * 85
            h = min(120, int(r['calls'] / 10))
            canvas.create_rectangle(x, 350 - h, x + 40, 350, fill="blue")
            canvas.create_text(x + 20, 365, text=f"n={r['n']}")
            
        print("\nPlot window opened successfully via built-in Tkinter.")
        root.mainloop()
    except Exception as e:
        print(f"\nPlotting skipped (headless environment detected): {e}")


    # ==============================================================================
    # PART 3: MATHEMATICAL ANALYSIS & RECURRENCE SUMMARY
    # Scope: Print analytical recurrences, complexity classes, and n=1000 estimates.
    # ==============================================================================
    
    def print_analysis():
        print("--- PART 3: MATHEMATICAL ANALYSIS ---")
        print("• Recurrences: T_A(n) = 1 + T_A(n-1) + T_A(n-2) | T_B(n) = 2n - 1")
        print("• Formula Proof: calls(n) = 2 * F(n+1) - 1 (Exponential O(phi^n))")
        print("• Complexity: Algo A is Exponential O(2^n); Algo B is Linear O(n).")
        print("• n = 1000 Estimate for Algo A: ~4.34 * 10^208 calls (Infeasible, >10^194 years).\n")
