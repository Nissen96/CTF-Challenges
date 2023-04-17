#include "aes.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char* KEY = "bprsuyndnuecrkne";

void print_hex(char* arr, int len) {
	for (int i = 0; i < len; i++) {
		printf("%02x ", (unsigned char)arr[i]);
	}
	printf("\n");
}

int main() {
	// Read specified file
	char msg[1024];
	FILE *fd = fopen("flag.txt", "r");
	fgets(msg, 1024 - 16, fd);

	// Pad plaintext
	int msglen = strlen(msg);
	int padding = 16 - (msglen % 16);
	for (int i = 0; i < padding; i++) {
		msg[msglen + i] = padding;
	}
	int padded_len = msglen + padding;

	// time_t now = time(NULL);  // Current time - what participants get
	time_t now = 1681558662;  // Hardcoded seed for chall generation
	printf("Seed: %d\n", now);
	srand(now);

	uint8_t iv[16];
	for (int i = 0; i < 16; i++) {
		iv[i] = rand();
	}

	// Setup AES-CBC
	struct AES_ctx ctx;
	
	AES_init_ctx_iv(&ctx, KEY, iv);

	// Encrypt
	AES_CBC_encrypt_buffer(&ctx, msg, padded_len);
	print_hex(msg, padded_len);

	// Decrypt
/*	AES_ctx_set_iv(&ctx, iv);
	AES_CBC_decrypt_buffer(&ctx, msg, msglen + padding);
	print_hex(msg, padded_len); */

	return 0;
}
