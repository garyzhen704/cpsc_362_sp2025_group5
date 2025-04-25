class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.is_face_down = False
        self.image = self.get_image_url()
        

    # represents the card as a "rank of suit"
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    
    def to_dict(self):
        # Convert the card to a dictionary format, also include the image URL
     return {
        'suit': self.suit,
        'rank': self.rank,
        'image': self.get_image_url(),
        'is_face_down':self.is_face_down
        }
    
        # creates a dictionary from a Card object
    @classmethod
    def from_dict(cls, data):
        return cls(data['rank'], data['suit'])
    
    def get_image_url(self):
        # Convert rank and suit to an appropriate filename for the card image
        if self.is_face_down:
            return 'poker_cards/bicycle_blue.svg' 
        rank_mapping = {
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10': '10',
            'J': 'jack', 'Q': 'queen', 'K': 'king', 'A': 'ace'
        }
        suit_mapping = {
            'hearts': 'hearts', 'diamonds': 'diamonds', 'clubs': 'clubs', 'spades': 'spades'
        }
        
        # Format the image filename: rank_of_suit.png
        rank_str = rank_mapping[self.rank]  # Get the correct rank string
        suit_str = suit_mapping[self.suit]  # Get the correct suit string

        # Construct the image URL path
        return f'poker_cards/{rank_str}_of_{suit_str}.png'