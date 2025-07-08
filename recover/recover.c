#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
 // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
 // Open the memory card with  (   fopen   )
    // Store the address of the opened file in a variable
    // r is for reading in binary mode
    FILE *input_file = fopen(argv[1], "r");
// Check if the file was opened successfully
    if (input_file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 2;
    }
// Store to the block of 512 bytes in a array
    unsigned char buffer[512];

// Track the number of JPEGs found
    int count_image = 0;
// File pointer for the output JPEG files
    FILE *output_file = NULL;

// char filename[8];
    char *filename = malloc(8 * sizeof(char));
// Read the blocks of 512 bytes
    while (fread(buffer, sizeof(char), 512, input_file))
    {
        // Check if bytes indicate start of JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Write the JPEG filenames
            sprintf(filename, "%03i.jpg", count_image);

            // Open output_file for writing
            output_file = fopen(filename, "w");

            // Count number of images found
            count_image++;
        }
        // Check if output has been used for valid input
        if (output_file != NULL)
        {
            // Write the buffer to the output file
            fwrite(buffer, sizeof(char), 512, output_file);
        }
    }
    free(filename);
    fclose(input_file);
    fclose(output_file);

    return 0;


}


