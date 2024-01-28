#include <iostream>
#include <SFML/Graphics.hpp>
#include <fstream>
#include <chrono>
#include <thread>

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

void updateAlbumCover(sf::Texture& album_art, sf::Sprite& albumSprite) {
    std::string album_cov = getCurrentSongFilePath();
    if (!album_cov.empty() && album_art.loadFromFile(album_cov)) {
        albumSprite.setTexture(album_art);
        albumSprite.setScale(sf::Vector2f(0.2, 0.2));
    } else {
        std::cerr << "Cannot load album cover.\n";
    }
}

int main() {
    sf::RenderWindow window(sf::VideoMode(sf::VideoMode::getDesktopMode().width + 100, sf::VideoMode::getDesktopMode().height), "SFML works!");
    window.setFramerateLimit(60); // Limit frame rate

    sf::RectangleShape album_cover(sf::Vector2f(140.f, 140.f));
    album_cover.setFillColor(sf::Color::Black);

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
    sf::Texture album_art;
    sf::Sprite albumSprite;
    updateAlbumCover(album_art, albumSprite);
    sf::Clock clock;
    double sleep_duration = readSleepDuration();

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
            else if (event.type == sf::Event::Resized) {
                window.setSize(sf::Vector2u(event.size.width, event.size.height));
                jukeBoxDisplay.setPosition(sf::Vector2f(x,y));
                albumSprite.setPosition(sf::Vector2f(sf::VideoMode::getDesktopMode().width/2 - 64, y+64));
            }
        }

        // Check if it's time to update the album cover
        if (clock.getElapsedTime().asSeconds() >= sleep_duration) {
            updateAlbumCover(album_art, albumSprite);
            clock.restart();
            sleep_duration = readSleepDuration(); // Read the sleep duration again
        }

        window.clear();
        window.draw(jukeBoxDisplay);
        window.draw(album_cover);
        window.draw(albumSprite);
        window.display();
    }

    return 0;
}