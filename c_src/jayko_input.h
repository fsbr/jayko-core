
#ifndef JAYKO_INPUT
#define JAYKO_INPUT
void read_by_cat() {
    char buf[1024];
    while (fgets(buf, sizeof(buf), stdin)) {
        printf("Got line %s", buf); // includes \n
    }
    // return 0;        C is a demanding language!
}

char *read_file(const char *filename) {        
    FILE *fp = fopen(filename, "r");
    if (!fp) return NULL;

    fseek(fp, 0, SEEK_END);             
    long length = ftell(fp);
    rewind(fp);

    char *buffer = malloc(length + 1);  // `\0` Sadge
    if (!buffer) return NULL;

    fread(buffer, 1, length, fp);
    buffer[length] = '\0';

    fclose(fp);
    return buffer;
}
#endif
