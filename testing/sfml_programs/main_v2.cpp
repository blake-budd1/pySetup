#include <iostream>
#include <SFML/Graphics.hpp>
#include <fstream>
#include <chrono>
#include <thread>
#include <vector>

std::string getCurrentSongFilePath() {
    std::ifstream file("../temp_files/current_song.txt");
    if (!file.is_open()) {
        std::cerr << "Error opening current_song.txt file.\n";
        return "";
    }
    std::string line;
    for (int i = 0; i < 2 && std::getline(file, line); ++i) {
        // Read the second line
        if (i == 1) {
            file.close();
            return line;
        }
    }

    file.close();
    return "";
}

std::string getCurrentName()
{
    std::ifstream file("../temp_files/current_song.txt");
    if (!file.is_open()) {
        std::cerr << "Error opening current_song.txt file.\n";
        return "";
    }
    std::string line;
    for (int i = 0; i < 4 && std::getline(file, line); ++i) {
        // Read the second line
        if (i == 3) {
            file.close();
            return line;
        }
    }

    file.close();
    return "";
}

std::string getNextSongFilePath()
{
    std::ifstream file("../temp_files/next_song.txt");
    if (!file.is_open())
    {
        std::cerr << "Error opening next_song.txt file. \n";
    }

    std::string line;
    for(int i = 0; i < 2 && std::getline(file, line); ++i)
    {
        if(i == 1)
        {
            file.close();
            return line;
        }
    }
    file.close();
    return "";
}

std::vector<std::string> getPreviousSongFilePaths()
{
    std::vector<std::string> previous_songs;
    std::ifstream file("../temp_files/previous_songs.txt");
    if(!file.is_open())
    {
        std::cerr << "Error opening previous_songs.txt file. \n";
    }

    std::string line;
    // need to loop through the previous songs and grab only the image urls.
    int curr_line = 0;
    for(int i = 0; std::getline(file, line); ++i)
    {
        // second line of each song entity is the image url
        if(curr_line == 1)
        {
            previous_songs.push_back(line);
        }
        // if the current line is the last one, then reset to 0 (new song element)
        if(curr_line == 7)
        {
            curr_line = 0;
        }
        else // otherwise, increment the current line by one. 
        {
            curr_line++;
        }
    }
    // std::cout << "previous songs:\n";
    // for(int i =0 ; i < previous_songs.size(); i++)
    // {
    //     std::cout << i << ". " << previous_songs[i] << "\n";
    // }
    return previous_songs;
}
std::string getPreviousSongFilePath()
{
     std::ifstream file("../temp_files/previous_songs.txt");
    if (!file.is_open())
    {
        std::cerr << "Error opening next_song.txt file. \n";
    }

    std::string line;
    for(int i = 0; i < 2 && std::getline(file, line); ++i)
    {
        if(i == 1)
        {
            file.close();
            return line;
        }
    }
    file.close();
    return "";
}



double readSleepDuration() {
    std::ifstream sleepFile("../temp_files/current_sleep.txt");
    double sleep_duration = 0.0;
    if (sleepFile.is_open()) {
        sleepFile >> sleep_duration;
        sleepFile.close();
        std::cout << "sleep duration is: " << sleep_duration << std::endl;
    } else {
        std::cerr << "Error opening current_sleep.txt file. Using default sleep duration.\n";
        sleep_duration = 2.0; // Default sleep duration in seconds
    }
    return sleep_duration;
}

void updateAlbumCover(sf::Texture& album_art, sf::Sprite& albumSprite, std::string& currName) {
    std::string album_cov = getCurrentSongFilePath();
    std::cout << "ALBUM COVER TO LOAD IS: " << album_cov << "\n";
    if (!album_cov.empty() && album_art.loadFromFile(album_cov)) {
        albumSprite.setTexture(album_art);
        albumSprite.setScale(sf::Vector2f(0.7, 0.7));
    } else {
        std::cerr << "Cannot load current album cover.\n";
    }
}


void updateNextAlbumCover(sf::Texture& nextAlbum_art, sf::Sprite& nextAlbumSprite)
{
    std::string next_cov = getNextSongFilePath();
    if(!next_cov.empty() && nextAlbum_art.loadFromFile(next_cov))
    {
        nextAlbumSprite.setTexture(nextAlbum_art);
        nextAlbumSprite.setScale(sf::Vector2f(0.6,0.6));
    }
    else{
        std::cerr << "cannot load next album cover. \n";
    }
}

void updatePreviousAlbumCover(sf::Texture& previousAlbum_art, sf::Sprite& previousAlbumSprite)
{
    std::string previous_cov = getPreviousSongFilePath();
    if(!previous_cov.empty() && previousAlbum_art.loadFromFile(previous_cov))
    {
        previousAlbumSprite.setTexture(previousAlbum_art);
        previousAlbumSprite.setScale(sf::Vector2f(0.6,0.6));
    }
    else{
        std::cerr << "cannot load next album cover. \n";
    }
}




int main() {
    sf::RenderWindow window(sf::VideoMode(sf::VideoMode::getDesktopMode().width + 100, sf::VideoMode::getDesktopMode().height), "SFML works!");
    window.setFramerateLimit(60); // Limit frame rate
    window.clear(sf::Color{0x240A09FF});

    sf::RectangleShape album_cover(sf::Vector2f(140.f, 140.f));
    album_cover.setFillColor(sf::Color{0xBB86FCFF});
    sf::RectangleShape prev_cover_background(sf::Vector2f(140.f, 140.f));
    prev_cover_background.setFillColor(sf::Color{0x3700B3FF});
    sf::RectangleShape next_cover_background(sf::Vector2f(140.f, 140.f));
    next_cover_background.setFillColor(sf::Color{0x3700B3FF});


    sf::Texture juke_box;
    if (!juke_box.loadFromFile("dependencies/jukebox.png")) {
        std::cerr << "Cannot load jukebox image.\n";
        return 1;
    }

    sf::Sprite jukeBoxDisplay;
    jukeBoxDisplay.setTexture(juke_box);
    jukeBoxDisplay.setScale(sf::Vector2f(0.2, 0.2));
    sf::Vector2u size = juke_box.getSize();
    size.x *= 0.2;
    size.y *= 0.2; // these get scaled later to 2
    int x = sf::VideoMode::getDesktopMode().width / 2 - (size.x/2);
    int y = sf::VideoMode::getDesktopMode().height - size.y;

    // start with the current album cover (only one available at start)
    sf::Texture album_art;
    sf::Sprite albumSprite;
    std::string currName;
    sf::Font font;
    if(!font.loadFromFile("dependencies/DMSans_36pt-Regular.ttf"))
    {
        std::cerr << "Error loading font" << std::endl;
    }
    updateAlbumCover(album_art, albumSprite, currName);
     // this stores the size of the sprite
    auto rect = albumSprite.getLocalBounds();

    sf::Clock clock;
    double sleep_duration = readSleepDuration();

    // get the next album cover (next in queue if available)
    sf::Texture next_album_art;
    sf::Sprite nextSprite;
    updateNextAlbumCover(next_album_art, nextSprite);
    auto next_size = nextSprite.getLocalBounds();

    // Create storage for the previous album covers:
    // these wont be initialized until the loop is ran, or after the first song is played. 
    sf::Texture previous_album_art;
    sf::Sprite previousSprite;
    updatePreviousAlbumCover(previous_album_art, previousSprite);

    auto prev_size = previousSprite.getLocalBounds();
    // for the sake of testing, previous_songs is hardcoded with values: get those now
    std::string current_songName = getCurrentName();
    std::cout << "current_name: " << current_songName << std::endl;
    sf::Text current_name_text;
    current_name_text.setFont(font);
    current_name_text.setString(current_songName);
    current_name_text.setScale(1.5f,1.5f);
    current_name_text.setFillColor(sf::Color::White);

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
            else if (event.type == sf::Event::Resized) {
                window.setSize(sf::Vector2u(event.size.width, event.size.height));
                jukeBoxDisplay.setPosition(sf::Vector2f(x,y));

                current_name_text.setString(current_songName);
                // set the position of the current album cover
                // update the album sprite to be at the middle
                albumSprite.setPosition(sf::Vector2f(sf::VideoMode::getDesktopMode().width/2 - (rect.width/4), y + 64));
                int albumSpriteEnd = sf::VideoMode::getDesktopMode().width/2 + (rect.width * 0.7) /2.5;
                album_cover.setSize(sf::Vector2f(rect.width *0.75, rect.height*0.75));
                album_cover.setPosition(sf::VideoMode::getDesktopMode().width/2 - (rect.width/3.625), (y+ 50));
                //std::cout << "screen width: " << sf::VideoMode::getDesktopMode().width << " \n";
                //std::cout << "album width: " << rect.width << "\n";               
                //std::cout << "starting position: " << sf::VideoMode::getDesktopMode().width/2 - rect.width/2 << "\n";
                //albumSprite.setPosition(sf::Vector2f(sf::VideoMode::getDesktopMode().width/2 - 64, y+64));
                // set the positions of the next album cover
                nextSprite.setPosition(sf::Vector2f (albumSpriteEnd + next_size.width/4, sf::VideoMode::getDesktopMode().height/2 - next_size.height/4));
                // set the positions of the previous album covers
                // starting position
                int albumSpriteStart = sf::VideoMode::getDesktopMode().width/2 - (rect.width * 0.7);
 
                previousSprite.setPosition(sf::Vector2f (albumSpriteStart - prev_size.width/4, sf::VideoMode::getDesktopMode().height/2 - prev_size.height/4));

                // set position and sizes of backgrounds for next and previous:
                next_cover_background.setSize(sf::Vector2f(next_size.width * 0.65, next_size.height * 0.65));
                next_cover_background.setPosition(sf::Vector2f(albumSpriteEnd + next_size.width/4.4, sf::VideoMode::getDesktopMode().height/2 - next_size.height/3.625));
              
                prev_cover_background.setSize(sf::Vector2f(prev_size.width * 0.65, prev_size.height * 0.65));
                prev_cover_background.setPosition(sf::Vector2f(albumSpriteStart - prev_size.width/3.6, sf::VideoMode::getDesktopMode().height/2 - prev_size.height/3.625));
               

                auto curr_name_size = current_name_text.getLocalBounds();
                current_name_text.setPosition(sf::Vector2f(sf::VideoMode::getDesktopMode().width/2  - curr_name_size.width + (curr_name_size.width/2 -curr_name_size.left) - 10  , 250));
            }
        }

        // Check if it's time to update the album cover
        if (clock.getElapsedTime().asSeconds() >= sleep_duration) {
            // update the current album cover
            updateAlbumCover(album_art, albumSprite, currName);
            // update the next album cover
            updateNextAlbumCover(next_album_art, nextSprite);
            // update the previous album covers
            updatePreviousAlbumCover(previous_album_art, previousSprite);

            // update the label of the new song
            current_songName = getCurrentName();
            // reset the clock to 0
            clock.restart();
            // read in the new sleep duration
            sleep_duration = readSleepDuration(); // Read the sleep duration again
        }

        window.clear(sf::Color{0x240A09FF});
        
        //window.draw(jukeBoxDisplay);
        // Draw current album cover
        // window.draw(album_cover);
        window.draw(album_cover);
        window.draw(albumSprite);
        // draw next album cover
        window.draw(next_cover_background);
        window.draw(nextSprite);
        // draw the previous album covers:
        window.draw(prev_cover_background);
        window.draw(previousSprite);
        window.draw(current_name_text);
        window.display();
    }

    return 0;
}
