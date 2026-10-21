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


