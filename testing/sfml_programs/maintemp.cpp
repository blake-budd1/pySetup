#include <iostream>
#include <SFML/Graphics.hpp>
#include <string>
#include <fstream>
#include <vector>
#include <chrono>
#include <thread>

std::string getCurrentSongFilePath() {
    // ... your existing code ...
}

std::vector<std::string> getPreviousSongFilePath() {
    // ... your existing code ...
}

void updateAlbumCover(sf::Texture& album_art, sf::Sprite& albumSprite) {
    std::string album_cov = getCurrentSongFilePath();
    std::cout << "Album cover: " << album_cov << std::endl;

    if (album_art.loadFromFile(album_cov)) {
        sf::Vector2u album_size = album_art.getSize();
        std::cout << "Album size: " << album_size.x << " | " << album_size.y << std::endl;

        albumSprite.setTexture(album_art);
        albumSprite.setPosition(sf::Vector2f(sf::VideoMode::getDesktopMode().width / 2 - 64, sf::VideoMode::getDesktopMode().height - 140));
        albumSprite.scale(sf::Vector2f(0.2, 0.2));
    } else {
        std::cerr << "Cannot load album cover.\n";
    }
}

int main() {
    sf::RenderWindow window(sf::VideoMode(sf::VideoMode::getDesktopMode().width + 100, sf::VideoMode::getDesktopMode().height), "SFML works!");
    sf::CircleShape shape(100.f);

    sf::RectangleShape album_cover(sf::Vector2f(140.f, 140.f));
    album_cover.setFillColor(sf::Color::Black);

    shape.setFillColor(sf::Color::Green);

    sf::Texture juke_box;
    if (!juke_box.loadFromFile("dependencies/jukebox.png"))
        std::cout << "Cannot load image.\n";

    sf::Texture album_art;
    sf::Sprite jukeBoxDisplay;
    jukeBoxDisplay.setTexture(juke_box);
    jukeBoxDisplay.setPosition(sf::Vector2f(sf::VideoMode::getDesktopMode().width / 2 - 64, sf::VideoMode::getDesktopMode().height - 140));
    jukeBoxDisplay.scale(sf::Vector2f(0.2, 0.2));

    sf::Sprite albumSprite;

    std::vector<std::string> previousSongs = getPreviousSongFilePath();
    std::cout << "Previous songs size: " << previousSongs.size() << "\n";

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        // Read the sleep duration from the file
        std::ifstream sleepFile("../temp_files/current_sleep.txt");
        double sleep_duration = 0.0;
        if (sleepFile.is_open()) {
            sleepFile >> sleep_duration;
            sleepFile.close();
        } else {
            std::cerr << "Error opening current_sleep.txt file. Using default sleep duration.\n";
        }

        // Ensure sleep duration is non-negative
        if (sleep_duration >= 0) {
            std::cout << "Sleeping for " << sleep_duration << " seconds...\n";
            std::this_thread::sleep_for(std::chrono::duration<double>(sleep_duration));
        } else {
            std::cerr << "Invalid sleep duration: " << sleep_duration << "\n";
            break;
        }

        // Update album cover and related information
        updateAlbumCover(album_art, albumSprite);

        window.clear();
        window.draw(jukeBoxDisplay);
        window.draw(album_cover);
        window.draw(albumSprite);
        window.display();
    }

    return 0;
}
