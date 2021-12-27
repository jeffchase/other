#include <stdio.h>
#include <math.h>

#define X_MIN (-2.5) 
#define X_MAX (2.5) 
#define Y_MIN (-4.0)
#define Y_MAX (1.0)

#define YSIZE 40
#define XSIZE 64

#define QX ((int)(XSIZE / (X_MAX - X_MIN)))
#define QY ((int)(YSIZE / (Y_MAX - Y_MIN)))

static int canvas[YSIZE][XSIZE];

int main(void)
{
	int x, y;
	double t;

	for (t = -3.14; t < 3.14; t += 0.01) {
		double r = sin(t) * sqrt(fabs(cos(t))) / (sin(t) + 7.0 / 5.0) -
		    2.0 * sin(t) + 2.0;
		x = (int)floor((r * cos(t) - X_MIN) * QX);
		y = (int)floor((r * sin(t) - Y_MIN) * QY);

		canvas[y][x]++;
	}

	for (y = YSIZE - 1; y >= 0; y--) {
		for (x = 0; x < XSIZE; x++)
			putchar(canvas[y][x] ? '.' : ' ');
		putchar('\n');
	}

	return 0;
}
