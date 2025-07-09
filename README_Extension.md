# Blackjack Chrome Extension

A complete Blackjack game that runs as a Chrome browser extension popup.

## Features

- **Complete Blackjack Game**: Standard rules with dealer AI
- **Visual Cards**: Styled card representations with suits and ranks
- **Betting System**: Start with $1000, place bets, track winnings
- **Auto-restart**: Automatic round reset after each game
- **Compact Design**: Optimized for 350x600 popup window

## Installation

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked" and select the folder containing these files
4. The Blackjack extension will appear in your extensions toolbar

## How to Play

1. **Place Bet**: Use the input field or quick bet buttons ($50, $100, $250, All-In)
2. **Deal**: Click "Deal" to start the round
3. **Play**: Choose "Hit" to draw cards or "Stand" to end your turn
4. **Win**: Beat the dealer without going over 21!

## Game Rules

- **Goal**: Get as close to 21 as possible without going over
- **Card Values**: Number cards = face value, Face cards = 10, Aces = 1 or 11
- **Dealer**: Must hit on 16, stand on 17+
- **Blackjack**: 21 with exactly 2 cards (pays 2.5:1)
- **Regular Win**: Pays 2:1
- **Push/Tie**: Bet returned (1:1)

## Files

- `manifest.json` - Chrome extension configuration
- `popup.html` - Game interface structure
- `popup.css` - Styling and layout
- `popup.js` - Game logic and functionality

## Technical Details

- Uses ES6+ JavaScript with object-oriented design
- No external dependencies
- Responsive design for popup constraints
- Smooth animations for card dealing
- Local storage not required (fresh game each time)

Enjoy playing Blackjack!
