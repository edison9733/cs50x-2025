// Todo greyscale, reflect, blur, edges


#include "helpers.h"
#include <math.h> // using round function
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // TODO  find average
    // row
    for (int i = 0; i < height ; i++)
    {
        //colummn
        for (int j = 0; j < width; j++)
        {
            // Convert pixels to float
            float Red = image[i][j].rgbtRed;
            float Green = image[i][j].rgbtGreen;
            float Blue = image[i][j].rgbtBlue;

            // Find average value
            int average = round((Red + Green + Blue) / 3);
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //TODO  reverse array
    for (int i = 0; i < height; i++)  // not affect height
    {
        // Swap pixels in each row
        for (int j = 0; j < width / 2; j++) // to avoid swapping back
        {
            // Temporary variable to hold pixel
            RGBTRIPLE temp = image[i][j];
            // Swap pixels
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    // Initialize temp with original image
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            temp[i][j] = image[i][j];
        }
    }

    // Calculate blurred pixels in temp
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            int red = 0, green = 0, blue = 0;
            float count = 0.0;

            for (int di = -1; di <= 1; di++) {
                for (int dj = -1; dj <= 1; dj++) {
                    int ni = i + di;
                    int nj = j + dj;

                    if (ni >= 0 && ni < height && nj >= 0 && nj < width) {
                        red += image[ni][nj].rgbtRed;
                        green += image[ni][nj].rgbtGreen;
                        blue += image[ni][nj].rgbtBlue;
                        count++;
                    }
                }
            }

            temp[i][j].rgbtRed = round(red / count);
            temp[i][j].rgbtGreen = round(green / count);
            temp[i][j].rgbtBlue = round(blue / count);
        }
    }

    // Copy temp back to image
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            image[i][j] = temp[i][j];
        }
    }
}

// Detect edges
void edges(int  height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    int Gx[3][3] ={
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };

    int Gy[3][3] = {
        {1, 2, 1},
        {0, 0, 0},
        {-1, -2, -1}
    };

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int redX, greenX, blueX;
            int redY, greenY, blueY;
            redX = greenX = blueX = 0;
            redY = greenY = blueY = 0;

            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 3; y ++)
                {
                    // Check for valid pixels
                    // i - 1 + x = currentX , J - 1 + y = currentY
                    if (i - 1 + x < 0 || i - 1 + x > height - 1 || j - 1 + y < 0 || j - 1 + y > width -1)
                    {
                        continue; // Skip invalid pixels
                    }
                    // Calculate Gx for each colour
                    redX += image[i - 1 + x][j - 1 + y].rgbtRed * Gx[i][j];
                    greenX += image[i - 1 + x][j - 1 + y].rgbtGreen * Gx[i][j];
                    blueX += image[i - 1 + x][j - 1 + y].rgbtBlue * Gx[i][j];
                    // Calculate Gy for each colour
                    redY += image[i - 1 + x][j - 1 + y].rgbtRed * Gy[i][j];
                    greenY += image[i - 1 + x][j - 1 + y].rgbtGreen * Gy[i][j];
                    blueY += image[i - 1 + x][j - 1 + y].rgbtBlue * Gy[i][j];


                }
            }
            // Calculate the value of square root of Gx2 and Gy2
            int red = round(sqrt(redX * redX + redY * redY));
            int green = round(sqrt(greenX * greenX + greenY * greenY));
            int blue = round(sqrt(blueX * blueX + blueY * blueY));

            // Clamp values to 255
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }

            temp[i][j].rgbtRed = red;
            temp[i][j].rgbtGreen = green;
            temp[i][j].rgbtBlue = blue;


        }
    }
    // Copy temp back to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }

    return;
}

