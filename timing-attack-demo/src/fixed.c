
// src/fixed.c
// Constant-time-ish comparison to remove timing leak for equal-length secrets.
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static const char *SECRET = "supersecret123"; // same secret as leaky

// Constant-time compare over the full max length (iterates through all bytes)
int constant_time_compare(const unsigned char *a, const unsigned char *b, size_t len) {
    unsigned char diff = 0;
    for (size_t i = 0; i < len; i++) {
        unsigned char ai = a[i];
        unsigned char bi = b[i];
        diff |= (unsigned char)(ai ^ bi);
    }
    return diff == 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <guess>\n", argv[0]);
        return 2;
    }
    const char *guess = argv[1];
    size_t len_s = strlen(SECRET);
    size_t len_g = strlen(guess);
    size_t len = (len_s > len_g) ? len_s : len_g;

    // Allocate zero-padded buffers so we always compare 'len' bytes.
    unsigned char *buf_s = (unsigned char*)calloc(len, 1);
    unsigned char *buf_g = (unsigned char*)calloc(len, 1);
    memcpy(buf_s, SECRET, len_s);
    memcpy(buf_g, guess, len_g);

    int ok = constant_time_compare(buf_s, buf_g, len);

    free(buf_s);
    free(buf_g);
    return ok ? 0 : 1;
}
