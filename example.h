
#ifndef EXAMPLE_H
#define EXAMPLE_H

#pragma pack(1)

#define BUFFER_SIZE 128
#define VERSION_MAJOR 1
#define VERSION_MINOR 0
#define VERSION ((VERSION_MAJOR << 8) | VERSION_MINOR)

typedef struct {
    unsigned char major;
    unsigned char minor;
} Version;

typedef struct {
    unsigned int magic;
    Version version;
    union {
        struct {
            unsigned char enabled : 1;
            unsigned char readonly : 1;
            unsigned char reserved : 6;
        } flags;
        unsigned char raw_flags;
    };
    char buffer[BUFFER_SIZE];
    unsigned int crc32;
} FileHeader;

#endif // EXAMPLE_H
