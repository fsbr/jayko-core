#include "jayko_array.h"

typedef struct {
    int x;
    int y;
} Point;
// this feels nontrivial because each function in codegen is going to need
// a way to print it.
DA_TYPEDEF(Point, PointArray)       // no semi colon. 

PointArray change_element(PointArray* xarr) {

    for (size_t i = 0; i < xarr->count; i++) {

        printf(" IN FUNCTION: x=%d, y=%d \n", xarr->items[i].x, xarr->items[i].y); 
    }

    xarr->items[0].x = 619;
    return *xarr;
}


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
    Point p4 = PointArray_get(&xs, 0, 0);
    printf(" hey again: x=%d, y=%d \n", p4.x, p4.y); 

    // Point p5 = PointArray_get(&xs, 4);       // these correctly give runtime errors!
    // Point p5 = PointArray_get(&xs, -1);


    PointArray xs2 = arbfun(&xs);
    for (size_t i = 0; i < xs.count; ++i) {
        printf(" xs2: x=%d, y=%d \n", xs2.items[i].x, xs2.items[i].y); 
        
    }
    // free the memory
    PointArray_free(&xs);
    return 0;
}



