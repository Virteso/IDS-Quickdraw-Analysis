#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if !defined(false)
#define false ((Bool)0)
#endif
#if !defined(true)
#define true ((Bool) !false)
#endif

#define DRSIZE 256

typedef unsigned char Bool;
typedef unsigned char Byte;

typedef struct stroke {
	unsigned short n_points;
	Byte *x;
	Byte *y;
} Stroke;

typedef struct drawing {
	unsigned long long key_id;
	char countrycode[3];
	Bool recognised;
	unsigned timestamp;
	unsigned short n_strokes;
	Stroke *strokes;
} Drawing;

void print_drawings(Drawing *drawings, int start, int howmuch)
{
	for (int i = start; i < start + howmuch; i++) {
		printf("{\n"
		       "\tkey_id: %llu,\n"
		       "\tcountrycode: %s,\n"
		       "\trecognised: %s,\n"
		       "\ttimestamp: %u,\n"
		       "\tn_strokes: %u,\n"
		       "\tstrokes: [\n",
		       drawings[i].key_id, drawings[i].countrycode,
		       drawings[i].recognised ? "true" : "false",
		       drawings[i].timestamp, drawings[i].n_strokes);
		for (int j = 0; j < drawings[i].n_strokes; j++) {
			printf("\t\tstroke %d: [\n", j);
			for (int k = 0; k < drawings[i].strokes[j].n_points;
			     k++) {
				printf("\t\t\t(x: %u, y: %u)\n",
				       drawings[i].strokes[j].x[k],
				       drawings[i].strokes[j].y[k]);
			}
			printf("\t\t]\n");
		}
		printf("\t]\n");
		printf("}\n");
	}
}

Drawing *unpack_drawing(FILE *file, Drawing *drawing)
{
	//printf("start reading at position %x\n", (unsigned)ftell(file));
	fread(&(drawing->key_id), 8, 1, file);
	fread(&(drawing->countrycode), 2, 1, file);
	// add null terminator to string in case drawing isnt 0-initted
	drawing->countrycode[2] = 0;
	fread(&(drawing->recognised), 1, 1, file);
	fread(&(drawing->timestamp), 4, 1, file);
	fread(&(drawing->n_strokes), 2, 1, file);
	drawing->strokes = malloc(sizeof(Stroke) * drawing->n_strokes);

	for (int i = 0; i < drawing->n_strokes; i++) {
		fread(&(drawing->strokes[i].n_points), 2, 1, file);
		drawing->strokes[i].x = malloc(drawing->strokes[i].n_points);
		drawing->strokes[i].y = malloc(drawing->strokes[i].n_points);
		fread(drawing->strokes[i].x, 1, drawing->strokes[i].n_points,
		      file);
		fread(drawing->strokes[i].y, 1, drawing->strokes[i].n_points,
		      file);
	}
	//printf("end reading at position %x\n", (unsigned)ftell(file));
	return drawing;
}

void unpack_drawings(const char *filename, Drawing *drawings, int n_drawings)
{
	FILE *file;
	file = fopen(filename, "rb");
	if (file == NULL) {
		printf("Couldn't open file ");
		perror(filename);
		exit(EXIT_FAILURE);
	}

	memset(drawings, 0, n_drawings * sizeof(drawings[0]));

	for (int i = 0; i < n_drawings; i++) {
		unpack_drawing(file, &drawings[i]);
	}
	fclose(file);
}

/// @brief Puts the strokes of a Drawing struct onto a 2D Byte array. The array should be Byte[256][256]
/// @param drawing drawing to copy strokes from
/// @param array 2D array where strokes are drawn
void put_drawing_strokes_on_2d_array(Drawing *drawing,
				     Byte array[DRSIZE][DRSIZE])
{
	// https://en.wikipedia.org/wiki/Digital_differential_analyzer_(graphics_algorithm)
	for (int skeit = 0; skeit < drawing->n_strokes; skeit++) {
		Stroke *stroke = &(drawing->strokes[skeit]);
		for (int j = 1; j < stroke->n_points; j++) {
			float p1x = (float)stroke->x[j - 1];
			float p1y = (float)stroke->y[j - 1];
			float p2x = (float)stroke->x[j];
			float p2y = (float)stroke->y[j];
			float dx = p2x - p1x;
			float dy = p2y - p1y;
			float step = abs(dx) >= abs(dy) ? abs(dx) : abs(dy);
			dx /= step;
			dy /= step;
			float xposition = p1x;
			float yposition = p1y;
			for (int k = 0; k <= step; k++) {
				array[(Byte)yposition][(Byte)xposition] = true;
				xposition += dx;
				yposition += dy;
			}
		}
	}
}

void save_drawing_pixel_array_into_npy_file(Byte array[DRSIZE][DRSIZE],
					    FILE *file)
{
	fwrite(array, DRSIZE * DRSIZE, 1, file);
}

void save_converted_drawings_to_npy_file(Drawing *drawings, int n_drawings,
					 const char *output_filename)
{
	if (fopen(output_filename, "r+") != NULL) {
		fprintf(stderr, "output file %s already exists\n",
			output_filename);
		exit(EXIT_FAILURE);
	}

	FILE *file = fopen(output_filename, "wb");
	Byte converted[DRSIZE][DRSIZE];
	memset(converted, 0, DRSIZE * DRSIZE);

	// input magic header
	fprintf(file, "\x93"
		      "NUMPY");

	fputc(1, file); // major version
	fputc(0, file); // minor version
	// length of the following python dict literal, hope it's not longer than this!
	fputc(99, file);
	fputc(0, file); // second byte of the length (unsigned short)
	// write the python dict header data
	fprintf(file,
		"{'descr': '|u1', 'fortran_order': False, 'shape': (%d, %d), }",
		n_drawings, DRSIZE * DRSIZE);
	// pad with spaces until header size is equal to what we specified
	// this feels like a stupid way to do this but it works for now
	while (ftell(file) != 128) fputc(' ', file);

	// write the actual file
	for (int i = 0; i < n_drawings; i++) {
		put_drawing_strokes_on_2d_array(&drawings[i], converted);
		save_drawing_pixel_array_into_npy_file(converted, file);
		memset(converted, 0, DRSIZE * DRSIZE);
	}
	fclose(file);
}

int main(int argc, const char **argv)
{
	enum {
		NONE,
		FILE,
		NDRAWINGS,
		OUTPUT,
	};

	int argmode = NONE;

	const char *drawingsfn = NULL;
	int ndrawings = -1;
	Bool printdrawings = false;
	const char *output_file = NULL;

	for (int i = 0; i < argc; i++) {
		if (strcmp(argv[i], "--help") == 0) {
			printf("Read a Quick! Draw dataset binary file into a .npy array file.\n"
			       "Arguments:\n"
			       "\t--file | -f\trequired, name of the source file (binary format)\n"
			       "\t--help\tshow this help text\n"
			       "\t-n\thow many drawings to load from the file\n"
			       "\t-output | -o\thow many drawings to load from the file\n"
			       "\t--print\tprint the read drawings\n");
			return 0;
		} else if (strcmp(argv[i], "-f") == 0
			   || strcmp(argv[i], "--file") == 0) {
			argmode = FILE;
			continue;
		} else if (strcmp(argv[i], "-n") == 0) {
			argmode = NDRAWINGS;
			continue;
		} else if (strcmp(argv[i], "--print") == 0) {
			printdrawings = true;
			continue;
		} else if (strcmp(argv[i], "-o") == 0
			   || strcmp(argv[i], "--output") == 0) {
			argmode = OUTPUT;
			continue;
		}
		switch (argmode) {
		case FILE:
			drawingsfn = argv[i];
			argmode = NONE;
			break;
		case NDRAWINGS:
			ndrawings = strtol(argv[i], NULL, 10);
			argmode = NONE;
			break;
		case OUTPUT:
			output_file = argv[i];
			argmode = NONE;
			break;
		}
	}

	if (drawingsfn == NULL) {
		fprintf(stderr, "need argument for filepath after --file\n");
		exit(EXIT_FAILURE);
	}
	if (ndrawings == -1) ndrawings = 1;

	Drawing drawings[ndrawings];
	unpack_drawings(drawingsfn, drawings, ndrawings);
	if (printdrawings) print_drawings(drawings, 0, ndrawings);
	save_converted_drawings_to_npy_file(drawings, ndrawings,
					    output_file == NULL ? "output.npy" :
								  output_file);

	return EXIT_SUCCESS;
}
