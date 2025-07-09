# Blackjack Game

A complete Blackjack game implementation in Python using tkinter for the graphical user interface.

## Features

- **Object-Oriented Design**: Clean, modular code with separate classes for cards, deck, hands, and game logic
- **Graphical Interface**: User-friendly GUI built with tkinter
- **Standard Blackjack Rules**: Implements all standard Blackjack gameplay rules
- **Automatic Ace Handling**: Aces automatically adjust between 1 and 11 values
- **Visual Card Display**: Cards displayed as text with suit symbols (♠, ♥, ♦, ♣)

## Classes

### Card
- Represents individual playing cards
- Handles rank, suit, and value calculations
- Face cards (J, Q, K) = 10, Aces = 11 (adjusted automatically)

### Deck
- Manages a standard 52-card deck
- Automatic shuffling and card dealing
- Auto-regenerates when empty

### Hand
- Holds cards and calculates hand values
- Intelligent Ace value adjustment (11 → 1 when needed)
- Detects busts and blackjacks

### BlackjackGame
- Main game controller with GUI
- Handles all game flow and user interactions
- Implements dealer AI (hits until 17+)

## Gameplay

1. **Start**: Player and dealer each get 2 cards (dealer's second card hidden)
2. **Player Turn**: Choose to "Hit" (draw card) or "Stand" (end turn)
3. **Dealer Turn**: Dealer reveals hidden card and draws until reaching 17+
4. **Winner**: Closest to 21 without going over wins

### Game Rules

- **Blackjack**: 21 with exactly 2 cards (Ace + 10-value card)
- **Bust**: Hand value exceeds 21 (automatic loss)
- **Push**: Tie when both have same value
- **Dealer Hits**: Dealer must hit on 16, stand on 17+

## Requirements

- Python 3.6+
- tkinter (included with Python)

## How to Run

```bash
python blackjack.py
```

## Controls

- **Hit**: Draw another card
- **Stand**: End your turn and let dealer play
- **Restart**: Start a new game

## Game Interface

The game window displays:
- Dealer's cards (one hidden until reveal)
- Player's cards (all visible)
- Current hand values
- Action buttons
- Game status messages

Enjoy playing Blackjack!
