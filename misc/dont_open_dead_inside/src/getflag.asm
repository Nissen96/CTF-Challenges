BITS 32

            org     0x08048000

ehdr:                                                 ; Elf32_Ehdr
            db      0x7F, "ELF", 1, 1, 1, 0         ;   e_ident
    times 8 db      0
            dw      2                               ;   e_type
            dw      3                               ;   e_machine
            dd      1                               ;   e_version
            dd      _start                          ;   e_entry
            dd      phdr - $$                       ;   e_phoff
            dd      0                               ;   e_shoff
            dd      0                               ;   e_flags
            dw      ehdrsize                        ;   e_ehsize
            dw      phdrsize                        ;   e_phentsize
            dw      1                               ;   e_phnum
            dw      0                               ;   e_shentsize
            dw      0                               ;   e_shnum
            dw      0                               ;   e_shstrndx

ehdrsize      equ     $ - ehdr

phdr:                                                 ; Elf32_Phdr
            dd      1                               ;   p_type
            dd      0                               ;   p_offset
            dd      $$                              ;   p_vaddr
            dd      $$                              ;   p_paddr
            dd      filesize                        ;   p_filesz
            dd      filesize                        ;   p_memsz
            dd      5                               ;   p_flags
            dd      0x1000                          ;   p_align

phdrsize      equ     $ - phdr

_start:
    push 112
    push 89
    push 38
    push 38
    push 85
    push 87
    push 39
    push 38
    push 87
    push 82
    push 102
    push 104
    push 35
    push 92
    push 86
    push 36
    push 95
    push 38
    push 87
    push 82
    push 38
    push 96
    push 35
    push 102
    push 82
    push 101
    push 35
    push 89
    push 82
    push 108
    push 101
    push 90
    push 97
    push 104
    push 91
    push 110
    push 89
    push 103
    push 86
    push 92
    mov ecx, 40
    call decrypt
    call print
    jmp exit
decrypt:
    add esp, 4
    add DWORD [esp], 13
    dec ecx
    cmp ecx, 0
    jne decrypt
    sub esp, 40*4
    ret
print:
    mov eax, 4
    mov ebx, 1
    add esp, 4
    mov ecx, esp
    sub esp, 4
    mov edx, 40*4
    int 0x80
    ret
exit:
    mov ebx,0
    mov eax,1
    int 0x80

filesize      equ     $ - $$
