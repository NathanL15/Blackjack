// Card Class
class Card {
    constructor(rank, suit) {
        this.rank = rank;
        this.suit = suit;
        this.value = this.calculateValue();
    }

    calculateValue() {
        if (['J', 'Q', 'K'].includes(this.rank)) {
            return 10;
        } else if (this.rank === 'A') {
            return 11; // Aces start as 11, adjusted in Hand class
        } else {
            return parseInt(this.rank);
        }
    }

    toString() {
        return `${this.rank}${this.suit}`;
    }

    getColor() {
        return ['♥', '♦'].includes(this.suit) ? 'red' : 'black';
    }
}

// Deck Class
class Deck {
    constructor() {
        this.cards = [];
        this.createDeck();
        this.shuffle();
    }

    createDeck() {
        const suits = ['♠', '♥', '♦', '♣'];
        const ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
        
        this.cards = [];
        for (const suit of suits) {
            for (const rank of ranks) {
                this.cards.push(new Card(rank, suit));
            }
        }
    }

    shuffle() {
        for (let i = this.cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.cards[i], this.cards[j]] = [this.cards[j], this.cards[i]];
        }
    }

    drawCard() {
        if (this.cards.length === 0) {
            this.createDeck();
            this.shuffle();
        }
        return this.cards.pop();
    }
}

// Hand Class
class Hand {
    constructor() {
        this.cards = [];
    }

    addCard(card) {
        this.cards.push(card);
    }

    getValue() {
        let total = 0;
        let aces = 0;

        for (const card of this.cards) {
            if (card.rank === 'A') {
                aces++;
                total += 11;
            } else {
                total += card.value;
            }
        }

        // Adjust for Aces
        while (total > 21 && aces > 0) {
            total -= 10;
            aces--;
        }

        return total;
    }

    isBusted() {
        return this.getValue() > 21;
    }

    isBlackjack() {
        return this.cards.length === 2 && this.getValue() === 21;
    }

    clear() {
        this.cards = [];
    }
}

// Game Manager Class
class GameManager {
    constructor() {
        this.deck = new Deck();
        this.playerHand = new Hand();
        this.dealerHand = new Hand();
        this.balance = 1000;
        this.currentBet = 0;
        this.gameOver = false;
        this.dealerHidden = true;
        this.animationSpeed = 500;

        this.initializeUI();
        this.setupEventListeners();
        this.updateDisplay();
    }

    initializeUI() {
        this.balanceEl = document.getElementById('balance');
        this.betInputEl = document.getElementById('bet-input');
        this.currentBetEl = document.getElementById('current-bet');
        this.dealerCardsEl = document.getElementById('dealer-cards');
        this.playerCardsEl = document.getElementById('player-cards');
        this.dealerValueEl = document.getElementById('dealer-value');
        this.playerValueEl = document.getElementById('player-value');
        this.dealBtn = document.getElementById('deal-btn');
        this.hitBtn = document.getElementById('hit-btn');
        this.standBtn = document.getElementById('stand-btn');
        this.statusEl = document.getElementById('game-status');
    }

    setupEventListeners() {
        // Bet buttons
        document.querySelectorAll('.bet-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const amount = e.target.dataset.amount;
                this.setBet(amount);
            });
        });

        // Control buttons
        this.dealBtn.addEventListener('click', () => this.dealCards());
        this.hitBtn.addEventListener('click', () => this.hit());
        this.standBtn.addEventListener('click', () => this.stand());
    }

    setBet(amount) {
        let newBet;
        if (amount === 'all') {
            newBet = this.balance;
        } else {
            const currentBet = parseInt(this.betInputEl.value) || 0;
            const addAmount = parseInt(amount);
            newBet = Math.min(currentBet + addAmount, this.balance);
        }
        this.betInputEl.value = newBet;
    }

    placeBet() {
        const bet = parseInt(this.betInputEl.value);
        
        if (!bet || bet <= 0) {
            alert('Bet must be greater than 0!');
            return false;
        }
        
        if (bet > this.balance) {
            alert("You don't have enough money!");
            return false;
        }

        this.currentBet = bet;
        this.balance -= bet;
        this.updateMoneyDisplay();
        return true;
    }

    updateMoneyDisplay() {
        this.balanceEl.textContent = `Balance: $${this.balance}`;
        if (this.currentBet > 0) {
            this.currentBetEl.textContent = `Current Bet: $${this.currentBet}`;
        } else {
            this.currentBetEl.textContent = '';
        }
    }

    payoutWinnings(multiplier) {
        const winnings = this.currentBet * multiplier;
        this.balance += winnings;
        this.updateMoneyDisplay();
    }

    checkGameOver() {
        if (this.balance <= 0) {
            alert("You're out of money! Game Over!");
            return true;
        }
        return false;
    }

    dealCards() {
        if (!this.placeBet()) return;

        this.disableBetting();
        this.statusEl.textContent = 'Dealing cards...';
        
        // Clear previous cards
        this.playerCardsEl.innerHTML = '';
        this.dealerCardsEl.innerHTML = '';
        
        // Reset hands
        this.playerHand.clear();
        this.dealerHand.clear();
        this.gameOver = false;
        this.dealerHidden = true;

        // Deal initial cards with animation
        this.dealInitialCards();
    }

    dealInitialCards() {
        const cardsToDeal = [
            { hand: this.playerHand, hidden: false },
            { hand: this.dealerHand, hidden: false },
            { hand: this.playerHand, hidden: false },
            { hand: this.dealerHand, hidden: true }
        ];

        this.dealCardsAnimated(cardsToDeal, 0, () => this.checkInitialBlackjack());
    }

    dealCardsAnimated(cardsToDeal, index, callback) {
        if (index >= cardsToDeal.length) {
            if (callback) callback();
            return;
        }

        const { hand } = cardsToDeal[index];
        const card = this.deck.drawCard();
        hand.addCard(card);

        // Only add the new card with animation
        this.addNewCardToDisplay(hand, card, hand === this.dealerHand);

        setTimeout(() => {
            this.dealCardsAnimated(cardsToDeal, index + 1, callback);
        }, this.animationSpeed);
    }

    addNewCardToDisplay(hand, newCard, isDealer) {
        const container = isDealer ? this.dealerCardsEl : this.playerCardsEl;
        const cardIndex = hand.cards.length - 1;
        const hideCard = isDealer && this.dealerHidden && cardIndex === 1;
        
        const cardEl = this.createCardElement(newCard, hideCard);
        cardEl.classList.add('new-card'); // Add animation class
        container.appendChild(cardEl);

        // Update hand value
        this.updateHandValue(hand, isDealer);

        // Remove animation class after animation completes
        setTimeout(() => {
            cardEl.classList.remove('new-card');
        }, 500);
    }

    checkInitialBlackjack() {
        this.enableButtons();

        if (this.playerHand.isBlackjack()) {
            if (this.dealerHand.isBlackjack()) {
                this.endGame('Push! Both have Blackjack!', 1);
            } else {
                this.endGame('Blackjack! Player Wins!', 2.5);
            }
        } else {
            this.statusEl.textContent = 'Choose Hit or Stand';
        }
    }

    hit() {
        if (this.gameOver) return;

        this.disableButtons();
        this.statusEl.textContent = 'Drawing card...';

        const card = this.deck.drawCard();
        this.playerHand.addCard(card);
        
        // Add only the new card with animation
        this.addNewCardToDisplay(this.playerHand, card, false);

        setTimeout(() => this.checkPlayerBust(), this.animationSpeed);
    }

    checkPlayerBust() {
        if (this.playerHand.isBusted()) {
            this.endGame('Player Busts! Dealer Wins!', 0);
        } else {
            this.enableButtons();
            this.statusEl.textContent = 'Choose Hit or Stand';
        }
    }

    stand() {
        if (this.gameOver) return;

        this.disableButtons();
        this.dealerHidden = false;
        this.statusEl.textContent = "Dealer's turn...";
        
        // Reveal dealer's hidden card
        this.revealDealerCard();

        setTimeout(() => this.dealerPlay(), this.animationSpeed);
    }

    revealDealerCard() {
        // Update the hidden card to show its actual value
        const dealerCards = this.dealerCardsEl.children;
        if (dealerCards.length > 1) {
            const hiddenCard = dealerCards[1];
            const card = this.dealerHand.cards[1];
            this.updateCardDisplay(hiddenCard, card);
        }
        this.updateHandValue(this.dealerHand, true);
    }

    dealerPlay() {
        if (this.dealerHand.getValue() < 17) {
            const card = this.deck.drawCard();
            this.dealerHand.addCard(card);
            
            // Add only the new card with animation
            this.addNewCardToDisplay(this.dealerHand, card, true);

            setTimeout(() => this.dealerPlay(), this.animationSpeed);
        } else {
            this.determineWinner();
        }
    }

    determineWinner() {
        const playerValue = this.playerHand.getValue();
        const dealerValue = this.dealerHand.getValue();

        if (this.dealerHand.isBusted()) {
            this.endGame('Dealer Busts! Player Wins!', 2);
        } else if (playerValue > dealerValue) {
            this.endGame('Player Wins!', 2);
        } else if (dealerValue > playerValue) {
            this.endGame('Dealer Wins!', 0);
        } else {
            this.endGame("Push! It's a Tie!", 1);
        }
    }

    endGame(message, payoutMultiplier) {
        this.gameOver = true;
        this.dealerHidden = false;
        this.updateDisplay();

        // Calculate winnings
        if (payoutMultiplier > 0) {
            this.payoutWinnings(payoutMultiplier);
            if (payoutMultiplier === 2.5) {
                message += ` (Blackjack bonus: +$${Math.floor(this.currentBet * 1.5)})`;
            } else if (payoutMultiplier === 2) {
                message += ` (+$${this.currentBet})`;
            } else if (payoutMultiplier === 1) {
                message += ` (Bet returned: $${this.currentBet})`;
            }
        }

        this.statusEl.textContent = message;
        
        // Auto-restart after 3 seconds
        setTimeout(() => this.autoRestartRound(), 3000);
    }

    autoRestartRound() {
        if (this.checkGameOver()) return;

        // Reset for next round
        this.playerHand.clear();
        this.dealerHand.clear();
        this.gameOver = false;
        this.dealerHidden = true;
        this.currentBet = 0;

        // Clear card displays
        this.playerCardsEl.innerHTML = '';
        this.dealerCardsEl.innerHTML = '';
        this.updateHandValue(this.playerHand, false);
        this.updateHandValue(this.dealerHand, true);
        
        this.updateMoneyDisplay();
        this.enableBetting();
        this.disableButtons();
        this.statusEl.textContent = 'Place your bet and click Deal for next round!';
    }

    updateDisplay() {
        this.drawHand(this.playerCardsEl, this.playerHand);
        this.updateHandValue(this.playerHand, false);

        if (this.dealerHidden && this.dealerHand.cards.length > 0) {
            this.drawHand(this.dealerCardsEl, this.dealerHand, true);
            this.dealerValueEl.textContent = 'Value: ?';
        } else {
            this.drawHand(this.dealerCardsEl, this.dealerHand);
            this.updateHandValue(this.dealerHand, true);
        }
    }

    updateHandValue(hand, isDealer) {
        const valueEl = isDealer ? this.dealerValueEl : this.playerValueEl;
        if (isDealer && this.dealerHidden && hand.cards.length > 0) {
            valueEl.textContent = 'Value: ?';
        } else {
            valueEl.textContent = `Value: ${hand.getValue()}`;
        }
    }

    updateCardDisplay(cardEl, card) {
        cardEl.className = `card ${card.getColor()}`;
        cardEl.innerHTML = `
            <div class="card-top">
                <div class="card-rank">${card.rank}</div>
                <div class="card-suit">${card.suit}</div>
            </div>
            <div class="card-center">${card.suit}</div>
            <div class="card-bottom">
                <div class="card-rank">${card.rank}</div>
                <div class="card-suit">${card.suit}</div>
            </div>
        `;
    }

    drawHand(container, hand, hideSecond = false) {
        container.innerHTML = '';

        hand.cards.forEach((card, index) => {
            const cardEl = this.createCardElement(card, hideSecond && index === 1);
            container.appendChild(cardEl);
        });
    }

    createCardElement(card, hidden = false) {
        const cardEl = document.createElement('div');
        cardEl.className = `card ${hidden ? 'hidden' : card.getColor()}`;

        if (hidden) {
            cardEl.innerHTML = '<div class="card-center">?</div>';
        } else {
            cardEl.innerHTML = `
                <div class="card-top">
                    <div class="card-rank">${card.rank}</div>
                    <div class="card-suit">${card.suit}</div>
                </div>
                <div class="card-center">${card.suit}</div>
                <div class="card-bottom">
                    <div class="card-rank">${card.rank}</div>
                    <div class="card-suit">${card.suit}</div>
                </div>
            `;
        }

        return cardEl;
    }

    enableButtons() {
        this.hitBtn.disabled = false;
        this.standBtn.disabled = false;
        this.dealBtn.disabled = true;
    }

    disableButtons() {
        this.hitBtn.disabled = true;
        this.standBtn.disabled = true;
    }

    enableBetting() {
        this.dealBtn.disabled = false;
        this.betInputEl.disabled = false;
    }

    disableBetting() {
        this.dealBtn.disabled = true;
        this.betInputEl.disabled = true;
    }
}

// Initialize game when popup loads
document.addEventListener('DOMContentLoaded', () => {
    new GameManager();
});
