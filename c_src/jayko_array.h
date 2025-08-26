// Header File for jayko's dynamic array.  
// Based on Tsoding's viral clip.


#ifndef JAYKO_ARRAY_H
#define JAYKO_ARRAY_H

#include <stdlib.h>
#include <stdio.h>

#define DA_TYPEDEF(T, Name) \
    typedef struct { \
        T *items; \
        size_t count; \
        size_t capacity; \
    } Name; \
    \
    static inline void Name##_append(Name *xs, T value) { \
        if (xs->count >= xs->capacity) { \
            xs->capacity = xs->capacity == 0 ? 4 : xs->capacity *2; \
            xs->items = realloc(xs->items, xs->capacity*sizeof(*xs->items)); \
            if (!xs->items) { \
                perror("realloc failed"); \
                exit(1); \
            } \
        } \
        xs->items[xs->count++] = value; \
    } \
    \
    static inline void Name##_free(Name *xs) { \
        free(xs->items); \
        xs->items = NULL; \
        xs->count = 0; \
        xs->capacity = 0; \
    }\
    static inline T Name##_get(Name *xs, size_t index) { \
        if (index >= xs->count) { \
            fprintf(stderr, "Index %zu out of bounds (size: %zu)\n", index, xs->count);\
            exit(1);\
        } \
        return xs->items[index];\
    }
#endif
