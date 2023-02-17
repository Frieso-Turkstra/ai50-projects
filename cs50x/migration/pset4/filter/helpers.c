#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // loop over every pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // calculate gray colour by avg the amount of red, green and blue
            int avg = round((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0);
            // assign avg gray colour to pixel
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtBlue = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // loop over every pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // use algorithm to calculate sepia colours
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            // assing sepia colours to pixel
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int row = 0; row < height; row++)
    {
        // create temporary array for reflected row
        RGBTRIPLE reflected[width];
        // loop over image from right to left and append pixels from left to right in reflected
        for (int i = 0, j = width - 1; j >= 0; i++, j--)
        {
            reflected[i] = image[row][j];
        }
        // replace row in image with its reflected counterpart
        for (int i = 0; i < width; i++)
        {
            image[row][i] = reflected[i];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // copy image to temporary blurry version
    RGBTRIPLE blurry[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            blurry[i][j] = image[i][j];
        }
    }
    // loop over every pixel
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            int totalRed = image[row][col].rgbtRed;
            int totalGreen = image[row][col].rgbtGreen;
            int totalBlue = image[row][col].rgbtBlue;
            float neighbours = 1;
            
            if (col - 1 >= 0) //Left
            {
                totalRed += image[row][col - 1].rgbtRed;
                totalGreen += image[row][col - 1].rgbtGreen;
                totalBlue += image[row][col - 1].rgbtBlue;
                neighbours++;
                if (row - 1 >= 0)//Left-Up
                {
                    totalRed += image[row - 1][col - 1].rgbtRed;
                    totalGreen += image[row - 1][col - 1].rgbtGreen;
                    totalBlue += image[row - 1][col - 1].rgbtBlue;
                    neighbours++;
                }
                if (row + 1 < height)//Left-Down
                {
                    totalRed += image[row + 1][col - 1].rgbtRed;
                    totalGreen += image[row + 1][col - 1].rgbtGreen;
                    totalBlue += image[row + 1][col - 1].rgbtBlue;
                    neighbours++;
                }
            }
            if (row - 1 >= 0)//Up
            {
                totalRed += image[row - 1][col].rgbtRed;
                totalGreen += image[row - 1][col].rgbtGreen;
                totalBlue += image[row - 1][col].rgbtBlue;
                neighbours++;
            }
            if (row + 1 < height)//Down
            {
                totalRed += image[row + 1][col].rgbtRed;
                totalGreen += image[row + 1][col].rgbtGreen;
                totalBlue += image[row + 1][col].rgbtBlue;
                neighbours++;
            }
            if (col + 1 < width)//Right
            {
                totalRed += image[row][col + 1].rgbtRed;
                totalGreen += image[row][col + 1].rgbtGreen;
                totalBlue += image[row][col + 1].rgbtBlue;
                neighbours++;
                if (row - 1 >= 0)//Right-up
                {
                    totalRed += image[row - 1][col + 1].rgbtRed;
                    totalGreen += image[row - 1][col + 1].rgbtGreen;
                    totalBlue += image[row - 1][col + 1].rgbtBlue;
                    neighbours++;
                }
                if (row + 1 < height)//Right-Down
                {
                    totalRed += image[row + 1][col + 1].rgbtRed;
                    totalGreen += image[row + 1][col + 1].rgbtGreen;
                    totalBlue += image[row + 1][col + 1].rgbtBlue;
                    neighbours++;
                }
            }
            blurry[row][col].rgbtRed = round(totalRed / neighbours);
            blurry[row][col].rgbtGreen = round(totalGreen / neighbours);
            blurry[row][col].rgbtBlue = round(totalBlue / neighbours);
        }
    }

    // copy blurry version to image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blurry[i][j];
        }
    }
    return;
}
