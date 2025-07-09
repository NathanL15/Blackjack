"""
Blackjack Game with tkinter GUI
A complete implementation of Blackjack using object-oriented design.
"""

import tkinter as tk
from tkinter import messagebox
from random import shuffle


class Card:
    """Represents a playing card with rank, suit, and value."""
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self._calculate_value()
    
    def _calculate_value(self):
        """Calculate the numeric value of the card."""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Aces start as 11, adjusted in Hand class
        else:
            return int(self.rank)
    
    def __str__(self):
        """String representation of the card."""
        return f"{self.rank}{self.suit}"


class Deck:
    """Manages a collection of playing cards."""
    
    def __init__(self):
        self.cards = []
        self._create_deck()
        self.shuffle_deck()
    
    def _create_deck(self):
        """Create a standard 52-card deck."""
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))
    
    def shuffle_deck(self):
        """Shuffle the deck of cards."""
        shuffle(self.cards)
    
    def draw_card(self):
        """Draw and return the top card from the deck."""
        if not self.cards:
            # If deck is empty, create and shuffle a new one
            self._create_deck()
            self.shuffle_deck()
        return self.cards.pop()


class Hand:
    """Holds cards and calculates scores."""
    
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)
    
    def get_value(self):
        """Calculate the total value of the hand, handling Aces appropriately."""
        total = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.value
        
        # Adjust for Aces
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total
    
    def is_busted(self):
        """Check if the hand value exceeds 21."""
        return self.get_value() > 21
    
    def is_blackjack(self):
        """Check if the hand is a blackjack (21 with 2 cards)."""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def clear(self):
        """Remove all cards from the hand."""
        self.cards.clear()
    
    def __str__(self):
        """String representation of the hand."""
        return ' '.join(str(card) for card in self.cards)


class BlackjackGame:
    """Main game class that controls flow and GUI logic."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Blackjack Game")
        self.root.geometry("900x800")
        self.root.configure(bg='green')
        self.root.resizable(True, True)
        
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
        self.dealer_hidden = True
        self.balance = 1000
        self.current_bet = 0
        self.animation_speed = 800  # milliseconds
        
        self._create_gui()
        self._start_new_game()
    
    def _create_gui(self):
        """Create the GUI elements."""
        # Title
        title_label = tk.Label(self.root, text="♠ BLACKJACK ♥", 
                              font=('Arial', 24, 'bold'), 
                              fg='white', bg='green')
        title_label.pack(pady=20)
        
        # Balance and betting section
        money_frame = tk.Frame(self.root, bg='green')
        money_frame.pack(pady=10)
        
        self.balance_label = tk.Label(money_frame, text=f"Balance: ${self.balance}", 
                                     font=('Arial', 16, 'bold'), 
                                     fg='white', bg='green')
        self.balance_label.pack(side=tk.LEFT, padx=20)
        
        tk.Label(money_frame, text="Bet:", 
                font=('Arial', 14, 'bold'), 
                fg='white', bg='green').pack(side=tk.LEFT, padx=10)
        
        self.bet_var = tk.StringVar(value="10")
        self.bet_entry = tk.Entry(money_frame, textvariable=self.bet_var, 
                                 font=('Arial', 12), width=8)
        self.bet_entry.pack(side=tk.LEFT, padx=5)
        
        # Bet buttons
        bet_button_frame = tk.Frame(money_frame, bg='green')
        bet_button_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Button(bet_button_frame, text="$10", font=('Arial', 10), 
                 command=lambda: self._set_bet(10), width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(bet_button_frame, text="$25", font=('Arial', 10), 
                 command=lambda: self._set_bet(25), width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(bet_button_frame, text="$50", font=('Arial', 10), 
                 command=lambda: self._set_bet(50), width=4).pack(side=tk.LEFT, padx=2)
        tk.Button(bet_button_frame, text="All-In", font=('Arial', 10), 
                 command=lambda: self._set_bet(self.balance), width=6).pack(side=tk.LEFT, padx=2)
        
        self.current_bet_label = tk.Label(self.root, text="", 
                                         font=('Arial', 14, 'bold'), 
                                         fg='yellow', bg='green')
        self.current_bet_label.pack(pady=5)
        
        # Dealer section
        dealer_frame = tk.Frame(self.root, bg='green')
        dealer_frame.pack(pady=20)
        
        tk.Label(dealer_frame, text="Dealer:", 
                font=('Arial', 16, 'bold'), 
                fg='white', bg='green').pack()
        
        # Dealer cards canvas
        self.dealer_canvas = tk.Canvas(dealer_frame, width=700, height=130, 
                                      bg='green', highlightthickness=0)
        self.dealer_canvas.pack(pady=10)
        
        self.dealer_value_label = tk.Label(dealer_frame, text="", 
                                          font=('Arial', 14, 'bold'), 
                                          fg='yellow', bg='green')
        self.dealer_value_label.pack()
        
        # Player section
        player_frame = tk.Frame(self.root, bg='green')
        player_frame.pack(pady=20)
        
        tk.Label(player_frame, text="Player:", 
                font=('Arial', 16, 'bold'), 
                fg='white', bg='green').pack()
        
        # Player cards canvas
        self.player_canvas = tk.Canvas(player_frame, width=700, height=130, 
                                      bg='green', highlightthickness=0)
        self.player_canvas.pack(pady=10)
        
        self.player_value_label = tk.Label(player_frame, text="", 
                                          font=('Arial', 14, 'bold'), 
                                          fg='yellow', bg='green')
        self.player_value_label.pack()
        
        # Buttons
        button_frame = tk.Frame(self.root, bg='green')
        button_frame.pack(pady=30)
        
        self.deal_button = tk.Button(button_frame, text="Deal", 
                                    font=('Arial', 14, 'bold'),
                                    bg='gold', fg='black',
                                    width=10, command=self._deal_cards)
        self.deal_button.pack(side=tk.LEFT, padx=10)
        
        self.hit_button = tk.Button(button_frame, text="Hit", 
                                   font=('Arial', 14, 'bold'),
                                   bg='lightblue', fg='black',
                                   width=10, command=self._hit)
        self.hit_button.pack(side=tk.LEFT, padx=10)
        
        self.stand_button = tk.Button(button_frame, text="Stand", 
                                     font=('Arial', 14, 'bold'),
                                     bg='orange', fg='black',
                                     width=10, command=self._stand)
        self.stand_button.pack(side=tk.LEFT, padx=10)
        
        self.restart_button = tk.Button(button_frame, text="Reset Game", 
                                       font=('Arial', 14, 'bold'),
                                       bg='lightcoral', fg='black',
                                       width=10, command=self._reset_game)
        self.restart_button.pack(side=tk.LEFT, padx=10)
        
        # Game status
        self.status_label = tk.Label(self.root, text="", 
                                    font=('Arial', 16, 'bold'), 
                                    fg='yellow', bg='green')
        self.status_label.pack(pady=20)
    
    def _set_bet(self, amount):
        """Set the bet amount."""
        if amount <= self.balance:
            self.bet_var.set(str(amount))
    
    def _place_bet(self):
        """Place the bet and start the game."""
        try:
            bet = int(self.bet_var.get())
            if bet <= 0:
                messagebox.showerror("Invalid Bet", "Bet must be greater than 0!")
                return False
            if bet > self.balance:
                messagebox.showerror("Insufficient Funds", "You don't have enough money!")
                return False
            
            self.current_bet = bet
            self.balance -= bet
            self._update_money_display()
            return True
        except ValueError:
            messagebox.showerror("Invalid Bet", "Please enter a valid number!")
            return False
    
    def _update_money_display(self):
        """Update balance and bet displays."""
        self.balance_label.config(text=f"Balance: ${self.balance}")
        if self.current_bet > 0:
            self.current_bet_label.config(text=f"Current Bet: ${self.current_bet}")
        else:
            self.current_bet_label.config(text="")
    
    def _payout_winnings(self, multiplier):
        """Pay out winnings based on multiplier."""
        winnings = self.current_bet * multiplier
        self.balance += winnings
        self._update_money_display()
    
    def _check_game_over(self):
        """Check if player is out of money."""
        if self.balance <= 0:
            messagebox.showinfo("Game Over", "You're out of money! Game Over!")
            self.root.quit()
            return True
        return False
    
    def _start_new_game(self):
        """Start a new game (called at initialization)."""
        if self._check_game_over():
            return
            
        # Reset game state
        self.deck = Deck()
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.game_over = False
        self.dealer_hidden = True
        self.current_bet = 0
        
        # Update displays
        self._update_display()
        self._update_money_display()
        self._enable_betting()
        self._disable_buttons()
        self.status_label.config(text="Place your bet and click Deal to start!")
    
    def _reset_game(self):
        """Reset the entire game with fresh balance."""
        result = messagebox.askyesno("Reset Game", 
                                   "This will reset your balance to $1000. Continue?")
        if result:
            self.balance = 1000
            self._start_new_game()
    
    def _deal_cards(self):
        """Deal initial cards after bet is placed."""
        if not self._place_bet():
            return
        
        self._disable_betting()
        self.status_label.config(text="Dealing cards...")
        
        # Deal cards with animation
        self._deal_initial_cards()
    
    def _deal_initial_cards(self):
        """Deal initial cards with animation."""
        cards_to_deal = [
            (self.player_hand, False),  # Player first card
            (self.dealer_hand, False),  # Dealer first card
            (self.player_hand, False),  # Player second card
            (self.dealer_hand, True)    # Dealer second card (hidden)
        ]
        
        self._deal_cards_animated(cards_to_deal, 0, self._check_initial_blackjack)
    
    def _deal_cards_animated(self, cards_to_deal, index, callback=None):
        """Deal cards one by one with animation."""
        if index >= len(cards_to_deal):
            if callback:
                callback()
            return
        
        hand, is_hidden = cards_to_deal[index]
        card = self.deck.draw_card()
        hand.add_card(card)
        
        # Update display
        self._update_display()
        
        # Schedule next card
        self.root.after(self.animation_speed, 
                       lambda: self._deal_cards_animated(cards_to_deal, index + 1, callback))
    
    def _check_initial_blackjack(self):
        """Check for blackjack after initial deal."""
        self._enable_buttons()
        
        if self.player_hand.is_blackjack():
            if self.dealer_hand.is_blackjack():
                self._end_game("Push! Both have Blackjack!", 1)  # Return bet
            else:
                self._end_game("Blackjack! Player Wins!", 2.5)  # 3:2 payout
        else:
            self.status_label.config(text="Choose Hit or Stand")
    
    def _hit(self):
        """Player draws a card."""
        if not self.game_over:
            self._disable_buttons()
            self.status_label.config(text="Drawing card...")
            
            # Add card with animation
            card = self.deck.draw_card()
            self.player_hand.add_card(card)
            self._update_display()
            
            # Check for bust after animation
            self.root.after(self.animation_speed, self._check_player_bust)
    
    def _check_player_bust(self):
        """Check if player busted after hitting."""
        if self.player_hand.is_busted():
            self._end_game("Player Busts! Dealer Wins!", 0)
        else:
            self._enable_buttons()
            self.status_label.config(text="Choose Hit or Stand")
    
    def _stand(self):
        """Player stands, dealer plays."""
        if not self.game_over:
            self._disable_buttons()
            self.dealer_hidden = False
            self.status_label.config(text="Dealer's turn...")
            self._update_display()
            
            # Start dealer play with delay
            self.root.after(self.animation_speed, self._dealer_play)
    
    def _dealer_play(self):
        """Dealer draws cards according to rules with animation."""
        if self.dealer_hand.get_value() < 17:
            # Dealer needs to hit
            card = self.deck.draw_card()
            self.dealer_hand.add_card(card)
            self._update_display()
            
            # Continue dealer play after animation
            self.root.after(self.animation_speed, self._dealer_play)
        else:
            # Dealer is done, determine winner
            self._determine_winner()
    
    def _determine_winner(self):
        """Determine and announce the winner."""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        if self.dealer_hand.is_busted():
            self._end_game("Dealer Busts! Player Wins!", 2)
        elif player_value > dealer_value:
            self._end_game("Player Wins!", 2)
        elif dealer_value > player_value:
            self._end_game("Dealer Wins!", 0)
        else:
            self._end_game("Push! It's a Tie!", 1)
    
    def _end_game(self, message, payout_multiplier):
        """End the current game and display the result."""
        self.game_over = True
        self.dealer_hidden = False
        self._update_display()
        
        # Calculate winnings
        if payout_multiplier > 0:
            self._payout_winnings(payout_multiplier)
            if payout_multiplier == 2.5:
                message += f" (Blackjack bonus: +${int(self.current_bet * 1.5)})"
            elif payout_multiplier == 2:
                message += f" (+${self.current_bet})"
            elif payout_multiplier == 1:
                message += f" (Bet returned: ${self.current_bet})"
        
        self.status_label.config(text=message)
        self._disable_buttons()
        
        # Auto-restart for next round after showing results
        self.root.after(3000, self._auto_restart_round)
    
    def _auto_restart_round(self):
        """Automatically prepare for the next round."""
        # Check if player is out of money first
        if self._check_game_over():
            return
        
        # Reset for next round
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.game_over = False
        self.dealer_hidden = True
        self.current_bet = 0
        
        # Update displays
        self._update_display()
        self._update_money_display()
        self._enable_betting()
        self._disable_buttons()
        self.status_label.config(text="Place your bet and click Deal for next round!")
    
    def _update_display(self):
        """Update the display with current game state."""
        # Update player display
        self._draw_hand(self.player_canvas, self.player_hand)
        self.player_value_label.config(text=f"Value: {self.player_hand.get_value()}")
        
        # Update dealer display
        if self.dealer_hidden and len(self.dealer_hand.cards) > 0:
            # Show first card, hide second
            self._draw_hand(self.dealer_canvas, self.dealer_hand, hidden_first=True)
            self.dealer_value_label.config(text="Value: ?")
        else:
            self._draw_hand(self.dealer_canvas, self.dealer_hand)
            self.dealer_value_label.config(text=f"Value: {self.dealer_hand.get_value()}")
        
        # Clear status if game is ongoing
        if not self.game_over:
            self.status_label.config(text="")
    
    def _enable_buttons(self):
        """Enable hit and stand buttons."""
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.deal_button.config(state=tk.DISABLED)
    
    def _disable_buttons(self):
        """Disable hit and stand buttons."""
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
    
    def _enable_betting(self):
        """Enable betting controls."""
        self.deal_button.config(state=tk.NORMAL)
        self.bet_entry.config(state=tk.NORMAL)
    
    def _disable_betting(self):
        """Disable betting controls."""
        self.deal_button.config(state=tk.DISABLED)
        self.bet_entry.config(state=tk.DISABLED)
    
    def _draw_card_visual(self, canvas, card, x, y, hidden=False):
        """Draw a visual representation of a card on the canvas."""
        card_width = 70
        card_height = 100
        
        if hidden:
            # Draw card back
            canvas.create_rectangle(x, y, x + card_width, y + card_height, 
                                  fill='navy', outline='black', width=2)
            canvas.create_text(x + card_width//2, y + card_height//2, 
                             text='?', fill='white', font=('Arial', 24, 'bold'))
        else:
            # Determine card color
            color = 'red' if card.suit in ['♥', '♦'] else 'black'
            
            # Draw card background
            canvas.create_rectangle(x, y, x + card_width, y + card_height, 
                                  fill='white', outline='black', width=2)
            
            # Draw rank in top-left corner
            canvas.create_text(x + 12, y + 15, text=card.rank, 
                             fill=color, font=('Arial', 12, 'bold'), anchor='center')
            
            # Draw suit in top-left corner
            canvas.create_text(x + 12, y + 30, text=card.suit, 
                             fill=color, font=('Arial', 14), anchor='center')
            
            # Draw large suit in center
            canvas.create_text(x + card_width//2, y + card_height//2, 
                             text=card.suit, fill=color, font=('Arial', 36))
            
            # Draw rank in bottom-right corner (upside down)
            canvas.create_text(x + card_width - 12, y + card_height - 15, 
                             text=card.rank, fill=color, font=('Arial', 12, 'bold'), 
                             anchor='center')
            
            # Draw suit in bottom-right corner (upside down)
            canvas.create_text(x + card_width - 12, y + card_height - 30, 
                             text=card.suit, fill=color, font=('Arial', 14), 
                             anchor='center')
    
    def _draw_hand(self, canvas, hand, hidden_first=False):
        """Draw all cards in a hand on the canvas."""
        canvas.delete("all")  # Clear previous cards
        
        card_spacing = 80
        start_x = 10
        start_y = 10
        
        for i, card in enumerate(hand.cards):
            x = start_x + (i * card_spacing)
            is_hidden = hidden_first and i == 1  # Hide second card if specified
            self._draw_card_visual(canvas, card, x, start_y, hidden=is_hidden)
    
    def run(self):
        """Start the game loop."""
        self.root.mainloop()


def main():
    """Main function to start the game."""
    game = BlackjackGame()
    game.run()


if __name__ == "__main__":
    main()
