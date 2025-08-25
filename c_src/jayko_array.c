#include "jayko_array.h"

typedef struct {
    int x;
    int y;
} Point;

DA_TYPEDEF(Point, PointArray)       // no semi colon. 
                                    
int main(void) {
    PointArray xs = {};

    Point p1 = {69, 420};
    Point p2 = {269, 2420};
    Point p3 = {369, 3420};
    
    PointArray_append(&xs, p1);
    PointArray_append(&xs, p2);
    PointArray_append(&xs, p3);

    for (size_t i = 0; i < xs.count; ++i) {
        printf(" HELLO: x=%d, y=%d \n", xs.items[i].x, xs.items[i].y); 
    }

    PointArray_free(&xs);
    return 0;

}



