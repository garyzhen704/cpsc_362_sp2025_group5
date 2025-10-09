from flask import Flask, render_template, url_for, jsonify, request, session
from flask_socketio import SocketIO, join_room, leave_room, emit, Namespace
from flask import Blueprint
import random
from blackjack.game_system import GameSystem
from blackjack.card import Card
from blackjack.deck import Deck
from blackjack.player import Player
def generate_unique_room_id():
    return str(random.randint(1000, 9999))

# Define the Blueprint
blackjack_bp = Blueprint('blackjack', __name__, template_folder='templates', static_folder='static')


class TitleNamespace(Namespace):
    def on_connect(self):
        print('Title page connected')

    def on_disconnect(self):
        print('Title page disconnected')
    def on_host(self,data):
        if len(active_games) < 8998:
            userName = data['username']
            room = generate_unique_room_id()
            game_system = GameSystem()
            player = Player()
            player.name = userName
            playerid = player.playerid
            game_system.add_player(player)
            game_system.players[0].name = 'dealer'
            socket_id = request.sid

            active_games[room] = {'game_system': game_system , 
                          'players':[userName],
                          'players_ready': {userName:False},
                          'all_ready':False ,
                          'turn_order': 1,
                          'socket_ids':{playerid:socket_id}
                          }

            emit('render_game', {'username':data['username'], 'room':room, 'player_id':playerid})
        else:
            emit("no_space")
    def on_join(self,data):
        username = data['username']
    
        player = Player()
        socket_id = request.sid
        player.name = username
        playerid = player.playerid
        available_rooms = [room for room, details in active_games.items() if len(details['players']) < MAX_PLAYERS]
        if available_rooms:
            # Pick a random room from available rooms
            room = random.choice(available_rooms)
            if(active_games[room]['all_ready'] == True):
                emit('error', {'message': '1No available rooms to join.'})
                return
            active_games[room]['players'].append(username)
            active_games[room]['game_system'].add_player(player)
            active_games[room]['socket_ids'][playerid]= socket_id
            emit('render_game', {'username':data['username'], 'room':room, 'player_id':playerid})
        else:
         # If no available rooms, send error message
            emit('error', {'message': '2No available rooms to join.'})

    def on_join_with_id(self,data):
        username = data['username']
        room = data['room']
        player = Player()
        socket_id = request.sid
        player.name = username
        playerid = player.playerid
        print('HERE. player type: ',type(player))

        # Check if the room exists
        if room in active_games:
            if(active_games[room]['all_ready']==True):
                emit('error', {'message': '1No available rooms to join.'})
                return
            if len(active_games[room]['players']) < MAX_PLAYERS:
                print(active_games[room]['players'])
                active_games[room]['players'].append(username)
                print('right before adding:',type(player))
                active_games[room]['game_system'].add_player(player)
                print('after adding:',player)
                active_games[room]['socket_ids'][playerid] = socket_id
                for x in active_games[room]['game_system'].players:
                    print('player types', x)

                emit('render_game', {'username':data['username'], 'room':room, 'player_id':playerid})
            else:
                emit('error', {'message': 'Room is full.'})
        else:
            emit('error', {'message': 'Room does not exist.'})


class ScreenNamespace(Namespace):
    def on_connect(self):
        room = request.args.get('room')
        username = request.args.get('username')
        playerid = request.args.get('playerid')
        active_games[room]['socket_ids'][playerid] = request.sid
    
        game = active_games[room]
        game_state= active_games[room]['game_system']
        join_room(room) # Associates Client to a room
        players_data = []
        player_list = active_games[room]['players']
        for player in game_state.players:
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status':player.status,
                'balance': player.balance,
                'current_bet': player.currentBet,
                'double_down':player.canDoubleDown(player.hand),
                'player_bust':player.busted,
                'player_turn':player.turn,
                'result':player.result,
                'is_last':player.islast
            }
            players_data.append(player_data)
        turn_order = game['turn_order']
    # broadcast event based on specific room. Takes event function name and a data payload that it will use.
        emit('update_game_state', {'player_bust':False,'player_list_length': len(player_list), 'player_info': players_data, 'all_ready':game['all_ready'], 'turn_order':turn_order, 'socket_ids':active_games[room]['socket_ids'],'endgame':False}, room = room)

    def on_disconnect(self):
        print('doing nothing')
        
        print('Screen page disconnected')
        room = request.args.get('room')
        username = request.args.get('username')
        
        game_system = active_games[room]['game_system']
        playerid = request.args.get('playerid')
        current_player = None
        players_data = []

        for player in game_system.players:
            if player.playerid == playerid:
                game_system.players.remove(player)
                current_player = player
        print(active_games[room]['players'])
        active_games[room]['players'].remove(player.name)
        print(active_games[room]['players'])

        for player in game_system.players:
            print(player.name)
        
        for player in game_system.players:
            print('player type:', type(player))
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status':player.status,
                'balance': player.balance,
                'current_bet': player.currentBet,
                'double_down':player.canDoubleDown(player.hand),
                'player_bust':player.busted,
                'player_turn':player.turn,
                'result':player.result,
                'is_last':player.islast
            }
            players_data.append(player_data)
        player_list = active_games[room]['players']
        leave_room(room)

        emit('update_game_state',{'leaverID':current_player.playerid,'player_list_length': len(player_list),'turn_order':active_games[room]['turn_order'],'player_info': players_data, 'all_ready':active_games[room]['all_ready'], 'endgame':False}, room = room)

        




    def on_place_bet(self, data):
        value = int(data['value'])
        playerid = data['playerid']
        room = data['room']
        game = active_games[room]
        game_system = game['game_system']
        players_data = []
        current_player = None
        all_players_ready = True
        player_busted = False

        for player in game_system.players:
            if player.playerid == playerid:
                current_player = player
            
                if value > player.balance:
                    emit('error', {'message': 'Insufficient balance for this bet.'})
                    return
                else:
                    player.currentBet = value
                    player.status = 'ready'
    
        for player in game_system.players:
            if(player.name == 'dealer'):
                continue
            if player.status != 'ready':
                all_players_ready = False 
        if(all_players_ready):
            game_system.startGame()
            game_system.players[0].hand.cards[0].is_face_down = True
            game_system.players[1].turn = True
        for player in game_system.players:
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status': player.status,
                'balance': player.balance,
                'current_bet':player.currentBet,
                'double_down':player.canDoubleDown(player.hand),
                'player_bust':player.busted,
                'player_turn': player.turn,
                'result':player.result,
                'is_last':player.islast
            }
        
            players_data.append(player_data)
        player_list = active_games[room]['players']
        if(all_players_ready):
            game['all_ready'] = True
        
            emit('update_game_state',{'player_list_length': len(player_list),'turn_order':game['turn_order'],'player_info': players_data, 'all_ready':game['all_ready'], 'endgame':False}, room = room) 
        else:
        
            game['all_ready'] = False
            emit('update_game_state', {'player_bust':False,'player_list_length': len(player_list),'turn_order':game['turn_order'],'player_info': players_data, 'all_ready':game['all_ready'], 'endgame':False}, room = room)
    
    



    def on_removeUI(self,data):
        room = data['room']
        playerid = data['playerid']
        socket_id = data['socket_id']
        emit('removeUI', room=active_games[room]['socket_ids'][playerid])
     
    
    def on_createUI(self,data):
        room = data['room']
        playerid = data['playerid']
        game_system = active_games[room]['game_system']
        players_data = []

        for player in game_system.players:
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status':player.status,
                'balance': player.balance,
                'current_bet': player.currentBet,
                'double_down':player.canDoubleDown(player.hand),
                'player_bust':player.busted,
                'player_turn':player.turn,
                'result':player.result,
                'is_last':player.islast
            }
            players_data.append(player_data)
    
        
        emit('createUI', room=active_games[room]['socket_ids'][playerid])
    
    def on_double_event(self, data):
        room = data['room']
        gameroom = active_games[room]
        game = active_games[room]['game_system']
        playerid = data['playerid']
        current_player = None
        player_bust = None
        players_data = []
        round_over = False
    
        for player in game.players:
            if(player.playerid == playerid):
                current_player = player
                break
        if(current_player.canDoubleDown(current_player.hand)):
            game.processAction(current_player,'doubleDown',current_player.hand)
        current_player.turn = False

        if(current_player.hand.getValue() >21):
            player_bust = current_player.playerid
            current_player.busted = True
            current_player.result = 'bust'
    

        if(current_player == game.players[len(game.players) -1]):
                game.players[0].turn = True
                round_over = True
                current_player.islast =True
        else:
            game.players[game.players.index(current_player)+1].turn = True
    
            

        for player in game.players:
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status': player.status,
                'balance': player.balance,
                'current_bet':player.currentBet,
                'double_down':player.canDoubleDown(player.hand),
                'player_bust': player.busted,
                'player_turn':player.turn,
                'result':player.result,
                'is_last':player.islast
            }
            if(player_bust == player.playerid):
                player_data['player_bust']=True
            players_data.append(player_data)
        emit('update_game_state', {'all_ready':gameroom['all_ready'],'room':room, 'player_bust':False, 'player_list_length':len(gameroom['players']), 'player_info':players_data, 'turn_order':gameroom['turn_order'], 'round_over':round_over, 'endgame':False},room=room)

    def on_stand_event(self, data):
        room = data['room']
        gameroom = active_games[room]
        game = active_games[room]['game_system']
        playerid = data['playerid']
        current_player = None
        players_data = []
        round_over = False

        for player in game.players:
            if(player.playerid == playerid):
                current_player = player
                break

        current_player.busted = False
        current_player.turn = False

        if(current_player == game.players[len(game.players) -1]):
            game.players[0].turn = True
            round_over = True
            current_player.islast =True
        else:
            game.players[game.players.index(current_player)+1].turn = True
            gameroom['turn_order'] = gameroom['turn_order']

        for player in game.players:
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status': player.status,
                'balance': player.balance,
                'current_bet':player.currentBet,
                'double_down':player.canDoubleDown(player.hand),
                'player_bust': player.busted,
                'player_turn':player.turn,
                'result':player.result,
                'is_last':player.islast
            }
            players_data.append(player_data)
    
        emit('update_game_state', {'all_ready':gameroom['all_ready'],'room':room, 'player_bust':False, 'player_list_length':len(gameroom['players']), 'player_info':players_data, 'turn_order':gameroom['turn_order'], 'round_over':round_over, 'endgame':False},room=room)
    

    def on_call_server(self, data):
        print('IN call_server')
        room = data['room']
        player_info = data['player_info']
        round_over = data['round_over']
        turn_order = data['turn_order']
        player_list_length = data['player_list_length']
        emit('update_game_state',{'player_bust':data['player_bust'],'round_over':round_over,'player_list_length': player_list_length,'turn_order':turn_order,'player_info':player_info, 'all_ready':active_games[room]['all_ready'], 'endgame':False}, room=request.sid) #data['room']


    def on_update_endgame(self, data):
        room = data['room']
        emit('update_game_state',{'player_list_length':data['player_list_length'], 'turn_order':data['turn_order'], 'player_info':data['player_info'], 'all_ready':data['all_ready'], 'endgame':True}, room=request.sid) #room


        
    def on_dealer_play(self, data):
        print('IN dealer play')
        room = data['room']
        player_id = data['playerid']
        gameroom = active_games[room]
        current_player= None
        players_info = data['player_info']
        game_system = active_games[room]['game_system']
        for player in game_system.players:
            if(player.busted == False):
                game_system.dealerPlay()
        game_system.players[0].turn = False
        for card in game_system.players[0].hand.cards:
            if card.is_face_down == True:
                card.is_face_down = False
            print("HAHAHAHAH",card.is_face_down)
        if(game_system.players[0].hand.getValue() >21):
            game_system.players[0].busted = True
    
        winners_dict = game_system.determineWinner()
        players_data = []
        for player in game_system.players:
            if player.playerid ==player_id:
                current_player = player
        print('current player id: ',current_player.playerid)
        print(winners_dict.items())
        for player in game_system.players:
            if player.name == 'dealer':
                continue
            for x,y in winners_dict.items():
                print(f"playerid: {x}, result: {y}")
                if player.playerid == x:
                    
                    player.result = y
                    print('player results:',player.name,player.result)
                    
                    if(y == 'winner'):
                        player.balance = player.balance + player.currentBet
                    
                    elif(y == 'blackjack'):
                        player.balance = player.balance + (1.5*player.currentBet)
                    
                    elif(y == 'bust'):
                        player.balance = player.balance - player.currentBet
                    
                    elif(y == 'loser'):
                        player.balance = player.balance - player.currentBet
                    
                    elif(y == 'push'):
                        player.balance = player.balance
                    
    
        for player in game_system.players:
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status': '',
                'balance': player.balance,
                'current_bet':0,
                'double_down':False,
                'player_bust': False,
                'player_turn':False,
                'result':player.result,
                'is_last':player.islast
             
            }
            print('results:',player.result)
            players_data.append(player_data)
        print('check dealer hand:',game_system.players[0].hand.cards[0].get_image_url())
        print('check dealer hand:',game_system.players[0].hand.cards[0].is_face_down)

    
    
        emit('update_balance_results', {'all_ready':gameroom['all_ready'],'turn_order':gameroom['turn_order'], 'players_data':players_data, 'player_list_length':len(gameroom['players']), 'endgame':False}, room=room) #room


    def on_end_round(self, data):
        room = data['room']
        gameroom = active_games[room]
        game_system = active_games[room]['game_system']
        players_data = []
        player_length = len(gameroom['players'])
        game_system.deck = Deck()

        for player in game_system.players:
            player.hand.clearHand()
            player.adjusted_balance = False
            player.currentBet = 0
            player.status = ''
            player.turn = False
            player.busted = False
            player.result = ''
            player.balance = player.balance
            player.islast = False
            if(player.balance <= 0):
                player.balance = 100
            username_list = []
            for player in game_system.players:
                if player.name == 'dealer':
                    continue
                username_list.append(player.name)
        gameroom['game_system'] = gameroom['game_system']
        gameroom['players'] = username_list
        gameroom['all_ready'] = False
        gameroom['turn_order'] = 1

        for player in game_system.players:
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status': player.status,
                'balance': player.balance,
                'current_bet':player.currentBet,
                'double_down':player.canDoubleDown(player.hand),
                'player_bust':player.busted,
                'player_turn': player.turn,
                'is_last':player.islast
             }
        
    
            players_data.append(player_data)
        print(active_games[room]['all_ready'])
        emit('update_game_state', {'player_bust':False,'player_list_length': player_length,'turn_order':gameroom['turn_order'],'player_info': players_data, 'all_ready':gameroom['all_ready'], 'endgame':False}, room = request.sid)#room
    

    def on_chat_event(self,data):
        emit('update_chat', {'message': data['message']}, room = data['room'])
    





    def on_hit_event(self, data):
        room = data['room']
        gameroom = active_games[room]
        game = active_games[room]['game_system']
        playerid = data['playerid']
        current_player = None
        player_bust = None
        players_data = []
        round_over = False
    
        for player in game.players:
            if(player.playerid == playerid):
                current_player = player
                break
        game.processAction(current_player,'hit',current_player.hand)
    
        if(current_player.hand.getValue() >21):
            player_bust = current_player.playerid
            current_player.busted = True
            current_player.result = 'bust'
            current_player.turn = False

        if(current_player.hand.getValue() >21):
            if(current_player == game.players[len(game.players) -1]):
                game.players[0].turn = True
                round_over = True
                current_player.islast =True
            else:
                game.players[game.players.index(current_player)+1].turn = True
            gameroom['turn_order'] = gameroom['turn_order']
    
            

        for player in game.players:
            player_data = {
                'username': player.name,
                'user_id': player.playerid,
                'hand': [card.to_dict() for card in player.hand.cards],
                'player_status': player.status,
                'balance': player.balance,
                'current_bet':player.currentBet,
                'double_down':player.canDoubleDown(player.hand),
                'player_bust': player.busted,
                'player_turn':player.turn,
                'result':player.result,
                'is_last':player.islast
            }
            if(player_bust == player.playerid):
                player_data['player_bust']=True
            players_data.append(player_data)
        print("LOOK HERE", player_data)
        emit('hit-event-client', {'all_ready':gameroom['all_ready'],'room':room, 'player_bust':player_bust, 'player_list_length':len(gameroom['players']), 'player_info':players_data, 'turn_order':gameroom['turn_order'], 'round_over':round_over, 'endgame':False},room=room)
    
    


@blackjack_bp.route('/')
def index():
    print('lololol')
    return render_template('blackjack_title.html')

@blackjack_bp.route('/game')
def game():
    return render_template('game.html')

@blackjack_bp.route('/title')
def title():
    return render_template('blackjack_title.html')


game_system = GameSystem()
active_games = {}
MAX_PLAYERS = 5
