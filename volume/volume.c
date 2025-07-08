#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "rb");  // Changed to binary mode
    if (input == NULL)
    {
        printf("Could not open input file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "wb");  // Changed to binary mode
    if (output == NULL)
    {
        printf("Could not open output file.\n");
        fclose(input);
        return 1;
    }

    float factor = atof(argv[3]);

    // Copy header from input file to output file
    uint8_t header[HEADER_SIZE];
    if (fread(header, sizeof(uint8_t), HEADER_SIZE, input) != HEADER_SIZE)
    {
        printf("Could not read header from input file.\n");
        fclose(input);
        fclose(output);
        return 1;
    }
    if (fwrite(header, sizeof(uint8_t), HEADER_SIZE, output) != HEADER_SIZE)
    {
        printf("Could not write header to output file.\n");
        fclose(input);
        fclose(output);
        return 1;
    }

    // Read samples from input file and write updated data to output file
    int16_t buffer;
    while (fread(&buffer, sizeof(int16_t), 1, input) == 1)
    {
        // Update volume of sample
        buffer = (int16_t)(buffer * factor);

        // Write updated sample to new file
        if (fwrite(&buffer, sizeof(int16_t), 1, output) != 1)
        {
            printf("Error writing sample to output file.\n");
            fclose(input);
            fclose(output);
            return 1;
        }
    }

    // Check for read errors
    if (ferror(input))
    {
        printf("Error reading from input file.\n");
        fclose(input);
        fclose(output);
        return 1;
    }

    // Close files
    if (fclose(input) != 0)
    {
        printf("Error closing input file.\n");
        return 1;
    }
    if (fclose(output) != 0)
    {
        printf("Error closing output file.\n");
        return 1;
    }

    return 0;
}
