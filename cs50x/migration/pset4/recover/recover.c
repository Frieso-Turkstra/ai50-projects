#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

char *create_filename(int image_count);

typedef uint8_t BYTE;
int jpeg_count = 0;

int main(int argc, char *argv[])
{
    // check for correct num of arguments
    if (argc != 2)
    {
        printf("Usage: ./recover file.raw\n");
        return 1;
    }

    // remember file names
    char *infile = argv[1];

    // open file
    FILE *fptr = fopen(infile, "r");
    if (fptr == NULL)
    {
        fprintf(stderr, "Cannot open %s\n", infile);
        return 1;
    }

    BYTE block[512];
    FILE *ptr = NULL;
    int writing = 0;

    while (fread(block, sizeof(BYTE), 512, fptr))
    {
        //we found a new jpeg
        if (block[0] == 255 && block[1] == 216 && block[2] == 255)
        {
            // open new file and set writing to true
            char *file_name = create_filename(jpeg_count);
            ptr = fopen(file_name, "w");
            free(file_name);
            writing = 1;
            jpeg_count++;
        }

        if (writing)
        {
            // write block to current file
            fwrite(block, sizeof(BYTE), 512, ptr);
        }
    }
    fclose(ptr);
}

char *create_filename(int image_count)
{
    // return filename as "001.jpeg" depending on image_count
    char *file_name = malloc(9 * sizeof(char));
    int a = image_count / 100;
    int b = (image_count - a * 100) / 10;
    int c = image_count - a * 100 - b * 10;
    sprintf(file_name, "%i%i%i.jpg", a, b, c);
    return file_name;
}
