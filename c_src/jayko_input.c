#include<stdio.h>
#include<stdlib.h>
#include "jayko_input.h"


int main() {
    char *contents = read_file("jayko_array.h");
    char current_char = '\0';
    if (!contents) {
        printf("Error reading file\n");
        return 1;
    }

    // printf("File Contents:\n%s\n", contents);

    int i = 0;
    while (contents[i] != '\0') {
        current_char = contents[i]; 
        if (current_char == 'c') printf("%c", current_char);
        i+=1;
    }
    //read_by_cat();
    return 0;
}
