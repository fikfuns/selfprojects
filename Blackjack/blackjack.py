import random
playerIn = True
dealerIn = True

# Player dealer hand
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 6, 7, 8, 9, 10,
        'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A', 'J', 'Q', 'K', 'A']
playerHand = []
dealerHand = []


# Dealing the cards
def deal_card(turn):
    card = random.choice(deck)
    turn.append(card)
    deck.remove(card)

# Calculate total of hand of player
def total(turn):
    total = 0
    face_cards = ['J', 'Q', 'K']
    for card in turn:
        if card in range(1, 11):
            total += card
        elif card in face_cards:
            total += 10
        # Coding 'A' or Ace card
        else:
            if total > 11:
                total += 1
            else:
                total += 11
    return total

# Check whether player/dealer won
def revealDealerHand():
    if len(dealerHand) == 2:
        return dealerHand[0]
    elif len(dealerHand) > 2:
        return dealerHand[0], dealerHand[1]

# combine all the 4 above into a game loop
for _ in range(2):
    deal_card(dealerHand)
    deal_card(playerHand)

while playerIn or dealerIn:
    print(f"Dealer had {revealDealerHand()} and X")
    print(f"You have {playerHand} for a total of {total(playerHand)}")
    if playerIn:
        stayOrHit = input("1: Stay\n2: Hit\n")
    if total(dealerHand) > 16:
        dealerIn = False
    else:
        deal_card(dealerHand)
    if stayOrHit == '1':
        playerIn = False
    else:
        deal_card(playerHand)
    if total(playerHand) >= 21:
        break
    elif total(dealerHand) >= 21:
        break

# See if dealer/player get blackjack
if total(playerHand) == 21:
    print(f"\n You have {playerHand} for a total of {total(playerHand)}\nThe dealer has {dealerHand} for a total of {total(dealerHand)}")
    print("Blackjack! You win!")
elif total(dealerHand) == 21:
    print(f"\n You have {playerHand} for a total of {total(playerHand)}\nThe dealer has {dealerHand} for a total of {total(dealerHand)}")
    print("Blackjack, but not for you. Dealer wins!")
# Player bust
elif total(playerHand) > 21:
    print(f"\n You have {playerHand} for a total of {total(playerHand)}\nThe dealer has {dealerHand} for a total of {total(dealerHand)}")
    print("You bust. Dealer wins!")
elif total(dealerHand) > 21:
    print(f"\n You have {playerHand} for a total of {total(playerHand)}\nThe dealer has {dealerHand} for a total of {total(dealerHand)}")
    print("Dealer busts. You win!")
# Check whos closer to 21
elif 21 - total(dealerHand) < 21 - total(playerHand):
    print(f"\n You have {playerHand} for a total of {total(playerHand)}\nThe dealer has {dealerHand} for a total of {total(dealerHand)}")
    print("Dealer wins! Better luck next time.")
elif 21 - total(dealerHand) > 21 - total(playerHand):
    print(f"\n You have {playerHand} for a total of {total(playerHand)}\nThe dealer has {dealerHand} for a total of {total(dealerHand)}")
    print("You win! Luck is on your side!")

