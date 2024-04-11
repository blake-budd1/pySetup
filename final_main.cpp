#include <iostream>
#include <SFML/Graphics.hpp>
#include <fstream>
#include <chrono>
#include <thread>
#include <vector>
#include <string>

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


std::string getHardwareID()
{
    std::ifstream file("../temp_files/hardware_id.txt");
    if(!file.is_open())
    {
        std::cerr << "Error opening hardware_id file.\n";
        return "";
    }
    std::string line;
    std::getline(file, line);
    file.close();
    return line;
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

bool readSFMLController(){
    std::ifstream sfmlControlFile("../temp_files/system_sfml_controller.txt");
    if(sfmlControlFile.is_open())
    {
        std::string line;
        while(std::getline(sfmlControlFile, line))
        {
            if(line == "update"){
                // clear the file  - 3/22 should be updated to clear the correct file
                std::ofstream clear_file("../temp_files/system_sfml_controller.txt",std::ios::out | std::ofstream::trunc);
                std::cout << "Cleared SFML controller file. \n";
                clear_file.close();
                return true;
            }
        }
    }
    else
    {
        std::cerr << "Error opening sfml control file.\n";
    }
    return false;
}


double readSleepDuration() {
    std::ifstream sleepFile("../temp_files/current_sleep.txt");
    double sleep_duration = 0.0;
    if (sleepFile.is_open()) {
        sleepFile >> sleep_duration;
        sleepFile.close();
       // std::cout << "sleep duration is: " << sleep_duration << std::endl;
    } else {
        std::cerr << "Error opening current_sleep.txt file. Using default sleep duration.\n";
        sleep_duration = 2.0; // Default sleep duration in seconds
    }
    return sleep_duration;
}



void updateAlbumCover(sf::Texture& album_art, sf::Sprite& albumSprite, std::string& currName) {
    std::string album_cov = getCurrentSongFilePath();
    //std::cout << "ALBUM COVER TO LOAD IS: " << album_cov << "\n";
    if (!album_cov.empty() && album_art.loadFromFile(album_cov)) {
        albumSprite.setTexture(album_art);
        albumSprite.setScale(sf::Vector2f(0.7, 0.7));
    } else {
        albumSprite.setScale(sf::Vector2f(0.7,0.7));
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
        nextAlbumSprite.setScale(sf::Vector2f(0,0));
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
        previousAlbumSprite.setScale(sf::Vector2f(0,0));
        std::cerr << "cannot load next album cover. \n";
    }
}




int main() {

    // On start up, wait here until an update to SFML has been read:
    bool start = false;
    int k = 0;
    while(!start){
        if(k < 15)
            k++;
        else
            // Read SFML controller into start
            start = readSFMLController();       
    }
    // This will not start until there are songs on the queue.

    sf::RenderWindow window(sf::VideoMode(sf::VideoMode::getDesktopMode().width + 100, sf::VideoMode::getDesktopMode().height), "The Modern Jukebox");
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

    //auto prev_size = previousSprite.getLocalBounds();
    // for the sake of testing, previous_songs is hardcoded with values: get those now
    std::string current_songName = getCurrentName();
    // std::cout << "current_name: " << current_songName << std::endl;
    sf::Text current_name_text;
    current_name_text.setFont(font);
    current_name_text.setString(current_songName);
    current_name_text.setScale(1.f,1.f);
    current_name_text.setFillColor(sf::Color::White);

    sf::Text hardware_id_text;
    hardware_id_text.setFont(font);
    hardware_id_text.setString("Session ID: " + getHardwareID());
    hardware_id_text.setScale(1.f, 1.f);
    hardware_id_text.setFillColor(sf::Color::White);

    bool updateData = false;
    int i = 0;
    while (window.isOpen()) {
        if (i == 15){
            // std::cout << "Read the SFML controller\n";
            updateData = readSFMLController();
             //std::cout << "Results are: " << updateData << "\n";
            i = 0;
        }
        else{
            i++;
        }
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
            else if (event.type == sf::Event::Resized) {
                window.setSize(sf::Vector2u(event.size.width, event.size.height));
                jukeBoxDisplay.setPosition(sf::Vector2f(x,y));
                auto prev_size = next_size;
                current_name_text.setString(current_songName);
                
                // update the album sprite to be at the middle
                albumSprite.setPosition(sf::Vector2f(sf::VideoMode::getDesktopMode().width/2 - (rect.width/4), y + 64));
                int albumSpriteEnd = sf::VideoMode::getDesktopMode().width/2 + (rect.width * 0.7) /2.5;
                album_cover.setSize(sf::Vector2f(rect.width *0.75, rect.height*0.75));
                album_cover.setPosition(sf::VideoMode::getDesktopMode().width/2 - (rect.width/3.625), (y+ 50));
                
                // set the positions of the next album cover
                nextSprite.setPosition(sf::Vector2f (albumSpriteEnd + next_size.width/4, sf::VideoMode::getDesktopMode().height/2 - next_size.height/4));

                // starting position
                int albumSpriteStart = sf::VideoMode::getDesktopMode().width/2 - (rect.width * 0.7);
 
                previousSprite.setPosition(sf::Vector2f (albumSpriteStart - prev_size.width/4, sf::VideoMode::getDesktopMode().height/2 - prev_size.height/4));

                // set position and sizes of backgrounds for next and previous:
                next_cover_background.setSize(sf::Vector2f(next_size.width * 0.65, next_size.height * 0.65));
                next_cover_background.setPosition(sf::Vector2f(albumSpriteEnd + next_size.width/4.4, sf::VideoMode::getDesktopMode().height/2 - next_size.height/3.625));
              
                prev_cover_background.setSize(sf::Vector2f(prev_size.width * 0.65, prev_size.height * 0.65));
                prev_cover_background.setPosition(sf::Vector2f(albumSpriteStart - prev_size.width/3.6, sf::VideoMode::getDesktopMode().height/2 - prev_size.height/3.625));
               

                sf::FloatRect curr_name_size = current_name_text.getLocalBounds();
                current_name_text.setOrigin(curr_name_size.left + curr_name_size.width/2.0f, curr_name_size.top + curr_name_size.height/2.0f);
                auto center = window.getView().getCenter();
                center.y -= 400;
                current_name_text.setPosition(sf::Vector2f(center.x, center.y));

                hardware_id_text.setPosition(sf::Vector2f(10,0));
            }
        }

        // Check if it's time to update the album cover
        // Update this to be a boolean, then each loop check the system_sfml_controller to check if it is 'update'
        // if it is, then run this stuff and clear the file. The queue handling will deal with updating this file. 

        if (updateData) {
            std::cout << "Updating data in sfml\n";
            // update the current album cover
            updateAlbumCover(album_art, albumSprite, currName);
            // update the next album cover
            updateNextAlbumCover(next_album_art, nextSprite);
            // update the previous album covers
            updatePreviousAlbumCover(previous_album_art, previousSprite);
            updatePreviousAlbumCover(previous_album_art, previousSprite);
            // update the label of the new song
            current_songName = getCurrentName();
            current_name_text.setString(current_songName);

            // read in the new sleep duration
            sleep_duration = readSleepDuration(); // Read the sleep duration again
            updateData = false;
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
        window.draw(hardware_id_text);
        window.display();

        
    }

    return 0;
}
