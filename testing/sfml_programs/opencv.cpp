#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>

using namespace cv;

//create image file with album
void createImage(std::string picture) {
   cv::Mat background = cv::imread("../dependencies/jukebox.png"); //, cv::IMREAD_UNCHANGED);
   cv::Mat prevImg = cv::imread(picture); //, cv::IMREAD_UNCHANGED);
   cv::Mat foreground;
   resize(prevImg, foreground, Size(400, 400), INTER_LINEAR);
   cv::Mat insetImage(background, cv::Rect(1800, 900, 400, 400));
   foreground.copyTo(insetImage);

   cv::imwrite("../combined.png", background);
}