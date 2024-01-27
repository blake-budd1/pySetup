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

    sf::Texture album_art;
    sf::Sprite albumSprite;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
            else if (event.type == sf::Event::Resized) {
                // Adjust the window and sprite positions on resize
                window.setSize(sf::Vector2u(event.size.width, event.size.height));
                jukeBoxDisplay.setPosition(sf::Vector2f(window.getSize().x / 2 - 64, window.getSize().y - 140));
                albumSprite.setPosition(sf::Vector2f(window.getSize().x / 2 - 64, window.getSize().y - 140));
            }
        }

        // Update album cover and related information
        updateAlbumCover(album_art, albumSprite);

        window.clear();
        window.draw(jukeBoxDisplay);
        window.draw(album_cover);
        window.draw(albumSprite);
        window.display();

        // Read the sleep duration from the file
        std::ifstream sleepFile("../temp_files/current_sleep.txt");
        double sleep_duration = 0.0;
        if (sleepFile.is_open()) {
            sleepFile >> sleep_duration;
            sleepFile.close();
        } else {
            std::cerr << "Error opening current_sleep.txt file. Using default sleep duration.\n";
            sleep_duration = 2.0; // Default sleep duration in seconds
        }

        // Ensure sleep duration is non-negative
        if (sleep_duration >= 0) {
            std::cout << "Sleeping for " << sleep_duration << " seconds...\n";
            std::this_thread::sleep_for(std::chrono::duration<double>(sleep_duration));
        } else {
            std::cerr << "Invalid sleep duration: " << sleep_duration << "\n";
            break;
        }
    }

    return 0;
}
