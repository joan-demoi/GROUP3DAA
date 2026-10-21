import sys
import time

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
# and generate visual representation using matplotlib (saves calls_plot.png).
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
    """Generates and saves calls_plot.png for the LaTeX report."""
    try:
        import matplotlib
        matplotlib.use('Agg')          # Important: works without a display
        import matplotlib.pyplot as plt

        n_A = [r['n'] for r in results_a]
        calls_A = [r['calls'] for r in results_a]
        n_B = [r['n'] for r in results_b]
        calls_B = [r['calls'] for r in results_b]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Algorithm A - log scale (required by the assignment)
        ax1.plot(n_A, calls_A, 'o-', color='red', linewidth=2, markersize=7, label='Algorithm A')
        ax1.set_yscale('log')
        ax1.set_xlabel('n')
        ax1.set_ylabel('Number of calls (log scale)')
        ax1.set_title('Algorithm A: Calls vs n\n(log y-scale required)')
        ax1.grid(True, which='both', linestyle='--', alpha=0.7)
        ax1.legend()

        # Algorithm B - normal scale
        ax2.plot(n_B, calls_B, 's-', color='blue', linewidth=2, markersize=7, label='Algorithm B')
        ax2.set_xlabel('n')
        ax2.set_ylabel('Number of calls')
        ax2.set_title('Algorithm B: Calls vs n')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()

        plt.tight_layout()
        plt.savefig('calls_plot.png', dpi=150, bbox_inches='tight')
        print("\n>>> SUCCESS: calls_plot.png has been created! <<<")
        plt.close()

    except ImportError:
        print("\nERROR: matplotlib is not installed.")
        print("Please run this command first:")
        print("    pip install matplotlib")
    except Exception as e:
        print(f"\nPlotting failed with error: {e}")


# ==============================================================================
# PART 3: MATHEMATICAL ANALYSIS & RECURRENCE SUMMARY
# Scope: Print analytical recurrences, complexity classes, and n=1000 estimates.
# ==============================================================================

def print_analysis():
    print("\n--- PART 3: MATHEMATICAL ANALYSIS ---")
    print("• Recurrences: T_A(n) = 1 + T_A(n-1) + T_A(n-2) | T_B(n) = 2n - 1")
    print("• Formula Proof: calls(n) = 2 * F(n+1) - 1 (Exponential O(phi^n))")
    print("• Complexity: Algo A is Exponential O(2^n); Algo B is Linear O(n).")
    print("• n = 1000 Estimate for Algo A: ~4.34 * 10^208 calls (Infeasible, >10^194 years).\n")


# ==============================================================================
# PART 4: RECURSION LIMIT FIXES & EDGE CASE ANALYSIS
# Scope: Handle recursion depth errors, propose fixes, and analyze `if fibtable[n]` check.
# ==============================================================================

def run_part4():
    print("--- PART 4: RECURSION LIMIT & EDGE CASES ---")
    print("• Default Failure: sys.getrecursionlimit() is 1000, causing RecursionError at n=1000.")
    print("• Fix 1: sys.setrecursionlimit(3000) (Risk: C-stack overflow if depth too high).")
    print("• Fix 2: Bottom-up iterative tabulation (Eliminates stack overhead entirely).")
    print("• Edge Case Check ('if fibtable[n]:'): For n=0, fibtable[0]=0 evaluates to False in Python.")
    print("  Correction: Use explicit 'if n in fibtable:' to prevent redundant base recomputations.\n")


# ==============================================================================
# PART 5: CONCLUSION & MAIN EXECUTION DRIVER
# Scope: Written summary on efficiency and overlapping subproblems, plus main driver.
# ==============================================================================

def print_conclusion():
    print("--- PART 5: CONCLUSION ---")
    print(
        "Algorithm B is infinitely more efficient than Algorithm A as n approaches 1000, "
        "reducing calls from 10^208 to 1,999 and execution time from millennia to <1ms.\n"
        "Principle: Overlapping Subproblems. Memoization caches computed states in a table, "
        "converting a redundant exponential call tree into an instantaneous O(1) Directed Acyclic Graph."
    )


def main():
    verify_base_equivalence()
    res_a, res_b = run_experiments()
    plot_results(res_a, res_b)
    print_analysis()
    run_part4()
    print_conclusion()


if __name__ == "__main__":
    main()
