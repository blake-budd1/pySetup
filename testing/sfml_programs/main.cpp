#include <iostream>
#include <SFML/Graphics.hpp>
#include <string>
#include <fstream>
#include <filesystem>
#include <vector>


// Need a function that can read in the second line of the current_song.txt to the location of the image 
std::string getCurrentSongFilePath(){
    // Storing the name of the current song image
    std::string image;
    // Need to open the file in temp_file/current_song.txt
    std::ifstream file("../temp_files/current_song.txt");
    if(!file.is_open())
    {
        std::cerr << "Error opening file. \n";
        return ""; // return an empty string indicating that the file could not be opened
    }

    std::string line;
    for(int i = 0;i < 2 && std::getline(file,line);++i)
    {
        // if we get to the second line that is the name of the song 
        std::cout << line << std::endl;
    }
    file.close();
    return line;
}

std::vector<std::string> getPreviousSongFilePath()
{
    std::string temp; // temp filepath for previous images (loops)
    std::vector<std::string> previousSongsImages;
    std::ifstream file("../temp_files/previous_songs.txt");
    if(!file.is_open()) // if this does not open, we are on the first song and there are no previous songs 
    {
        std::cout << "No previous song data available. \n";
    }   
    std::string line;
    bool readNextLine = false;
    while(std::getline(file, line))
    {
        if(readNextLine){
            previousSongsImages.push_back(line);
            std::cout << "Previous song url: " << line;
            readNextLine = false;
        }
        else
        {
            readNextLine = true;
        }
    }
    file.close();
    std::cout << "printing previous song data in function: \n";
    for(int i = 0 ; i < previousSongsImages.size(); i++) 
    {
        std::cout << "previous songs [" << i << "] = " << previousSongsImages[i];
    }
    return previousSongsImages;
}

int main()
{
    sf::RenderWindow window(sf::VideoMode(sf::VideoMode::getDesktopMode().width, sf::VideoMode::getDesktopMode().height), "SFML works!");
    sf::CircleShape shape(100.f);

    // rectangle to hold album cover in:
    sf::RectangleShape album_cover(sf::Vector2f(140.f, 140.f));
    album_cover.setFillColor(sf::Color::Black);

    shape.setFillColor(sf::Color::Green);
    // create image object for jukebox image
    sf::Texture juke_box;
    // load jukebox image into object: juke_box
    if (!juke_box.loadFromFile("dependencies/jukebox.png"))
        std::cout << "Cannot load image.\n";

    sf::Texture album_art;
    //std::string file_path = "../album_covers/";
    std::string album_cov = getCurrentSongFilePath();
    std::cout << "Album cover: " << album_cov << std::endl;

    // Load the album cover and store it into the texture for the album_art
    if (!album_art.loadFromFile(album_cov))
        std::cout << "cannot load album cover. \n";
    
    sf::Vector2u album_size = album_art.getSize();
    std::cout << "album size: " << album_size.x << " | " << album_size.y << std::endl;
    
    // height and width of the image to place in correct location:
    sf::Vector2u size = juke_box.getSize();
    size.x *= 0.2;
    size.y *= 0.2; // these get scaled later to 2
    std::cout << "size of the image: " << size.x << " | " << size.y << "\n";
    int x = sf::VideoMode::getDesktopMode().width / 2 - (size.x/2);
    int y = sf::VideoMode::getDesktopMode().height - size.y;


    // Handle getting all the images from the previous_songs.txt file if it exists
    std::vector<std::string> previousSongs = getPreviousSongFilePath();
    std::cout << "previousSongs.size() = " << previousSongs.size() << "\n";

    
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        //window.draw(shape);
        sf::Sprite jukeBoxDisplay;
        jukeBoxDisplay.setTexture(juke_box);
        jukeBoxDisplay.setPosition(sf::Vector2f(x,y));
        
        // Create sprite for the album cover:
        sf::Sprite albumSprite;
        albumSprite.setTexture(album_art);
        albumSprite.setPosition(sf::Vector2f(sf::VideoMode::getDesktopMode().width/2 - 64,y + 64));
        albumSprite.scale(sf::Vector2f(0.2, 0.2));

        jukeBoxDisplay.scale(sf::Vector2f(0.2, 0.2));
        window.clear();
        window.draw(jukeBoxDisplay);
        window.draw(album_cover);
        window.draw(albumSprite);
        window.display();
    }

    return 0;
}