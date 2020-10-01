# StarTheory
A text based space exploration and battle game

To run, run the StarTheory.py file. It's suggested that you use terminal's full screen mode. 

I am unsure if this prgram is compatible with Windows or Linux operating systems, as it uses some
formatting tools to change the colors in macOS terminal. 

## Overview
Star Theory is an entirely text-based game about a solitary space pilot journeying through galactic empires, trading, exploring, and fighting your way towards the rest of the artifacts needed to discover how the galaxy fell apart. Unfortunately, the exploring, artifacts, galactic factions, and story line are yet to be implemented. I stopped work when I realized that the largest barrier forward was the format of the game—text. I hope to rebuild this game in the future with the help of a system that supports graphics.

### Notable Aspects of the Game
* Fully modeled, simulated galaxy
  * Semi-random resource generation of over 500 planets across 150 star systems
  * Modeled population, technological progression, space traffic, and planetary exports and prices based off of distribution of resources, planets and proximity to one another
  * Fluctuating economy with (heavily exaggerated) responses to player purchases and sales, as well as random shortages and surpluses
    * Functioning systems for upgrading, purchasing, and trading on planets
* Combat system framework
  * Tactical, text-based combat
    * Reliant on knowledge of interaction of weapons and defenses
    * Dynamic and non-repetitive, both within individual combats, and over the course of the game
    * Enormously reusable and expandable
  * Gorgeous UI/UX
    * Unfortunately, it's still text based, which means typing all responses, no animations, and information primarily portrayed through words

### Programming Lessons Learned
The current version of Star Theory is the 4th complete rewrite; as I learn more, I refactor so my code better matches best practices in programming. Here are some general attributes of the latest version
* Largely decoupled classes
* Virtually no hardcoding
* Black-box principle implemented in nearly all classes and functions
* Proficient implementation of polymorphism
* High level of reusability in code
* Separate, debugging log tracks events during game
