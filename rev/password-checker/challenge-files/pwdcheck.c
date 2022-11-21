#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <unistd.h>

const int pwd_len = 53;
const int pwd_offset = 0x42;
const char masked[53] = {126, 126, 125, 181, 167, 110, 173, 165, 107, 168, 161, 153, 167, 179, 153, 170, 110, 173, 173, 177, 106, 172, 158, 153, 111, 162, 106, 175, 166, 158, 153, 156, 109, 153, 161, 106, 106, 158, 153, 109, 168, 106, 175, 161, 162, 153, 172, 107, 161, 162, 174, 121, 183};


bool check_password(char *pwd) {
  bool correct = true;
  for (int i = 0; i < pwd_len; i++) {
    if (pwd[i] != (char)(masked[i] - pwd_offset)) {
      correct = false;
    }
  }
  return correct;
}

int main() {
  char pwd[256];

  printf("Password: ");

  if (fgets(pwd, sizeof(pwd), stdin) == NULL) {
    printf("Error reading from stdin!\n");
    return -1;
  }

  printf("Validating...\n");
  sleep(1);

  if (check_password(pwd))
    printf("Permission granted!\n");
  else
    printf("Invalid password!\n");

  return 0;
}
