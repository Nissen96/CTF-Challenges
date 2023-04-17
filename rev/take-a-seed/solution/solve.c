#include "aes.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
	// Hardcoded ct
	char ct[] = {
		0x3c, 0x0f, 0xf3, 0x6e, 0xad, 0xa0, 0x55, 0x44, 0x43, 0xbb, 0xf9, 0x06, 0xa1, 0xd9, 0xee, 0xa2,
		0x1d, 0x74, 0x20, 0xad, 0xbf, 0xe0, 0xfc, 0x09, 0x46, 0x27, 0x3f, 0x1d, 0x47, 0x97, 0xb6, 0x6a,
		0x69, 0xf5, 0x83, 0x88, 0xb1, 0x60, 0x2b, 0x41, 0x5e, 0x22, 0x6f, 0xac, 0x24, 0x2e, 0x57, 0xfd,
		0xc9, 0x64, 0x17, 0x1b, 0xe6, 0x11, 0x84, 0xf8, 0x84, 0xcf, 0x2f, 0xcd, 0x9a, 0x45, 0x45, 0xfe
	};
	int len = sizeof(ct);
	char* key = "bprsuyndnuecrkne";
	uint8_t iv[16];
	struct AES_ctx ctx;
	char pt[len];

	// Bruteforce seed - actual: 1681385857
	for (time_t seed = 1681545600; seed < 1681581600; seed++) {
		srand(seed);
		for (int i = 0; i < 16; i++) {
			iv[i] = rand();
		}

		// Copy ct to pt as AES functions decrypt inplace
		memcpy(pt, ct, sizeof(ct));
		
		AES_init_ctx_iv(&ctx, key, iv);
		AES_CBC_decrypt_buffer(&ctx, pt, len);

		if (strncmp("DDC{", pt, 4) == 0) {
			// Optional unpadding by zeroing first padding byte
			int padding = pt[len - 1];
			pt[len - padding] = 0;

			printf("Seed: %d, msg: %s\n", seed, pt);
			break;
		}
	}

	return 0;
}