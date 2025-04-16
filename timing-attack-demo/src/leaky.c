
// src/leaky.c
// Insecure, timing-leaky string comparison demo.
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

static const char *SECRET = "supersecret123"; // demo secret

// Insecure compare: returns early on mismatch and sleeps per matched byte
int insecure_compare(const char *a, const char *b) {
    size_t i = 0;
    while (a[i] != '\0' && b[i] != '\0') {
        if (a[i] != b[i]) {
            return 0;
        }
        // artificial delay to amplify the leak
        usleep(2000); // 2ms per correct byte
        i++;
    }
    return a[i] == b[i];
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <guess>\n", argv[0]);
        return 2;
    }
    const char *guess = argv[1];
    int ok = insecure_compare(SECRET, guess);
    // Print nothing; the attacker only measures runtime.
    // Return code is 0 on success, 1 on failure for convenience.
    return ok ? 0 : 1;
}
