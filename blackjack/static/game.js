// Assuming you are using socket.io, initialize the socket connection here
const urlParams = new URLSearchParams(window.location.search);
  const roomCode = urlParams.get('room');
  const username = urlParams.get('username');
  const playerid = urlParams.get('playerid');
const socket = io('/game_screen', {
  query:{
    'room':roomCode,
    'username':username,
    'playerid':playerid
  }
});
function sleep(ms) {
  var start = new Date().getTime();
  while (new Date().getTime() - start < ms) {
      // Just keep looping until the time has passed
  }
}

  player_card_count = 0
  var socket_ids = {};
  var players_info_list = [];
  var client_player;
console.log('loaded page')
  
  // Extract both room and username from the URL
  document.getElementById('room-number').innerText = `Room#: ${roomCode}`;
  document.getElementById('player1-username').innerText = `Username: ${username}`;

//socket.emit('join_room', {'room':roomCode, 'username':username, 'userid':playerid})

  
window.addEventListener('beforeunload', () => {
  socket.disconnect();
});




  

socket.on('update_game_state', function(data){
    console.log('in update_game_state')
  const urlParams = new URLSearchParams(window.location.search);
  const roomCode = urlParams.get('room');
  const username = urlParams.get('username');
  const playerid = urlParams.get('playerid');
  turn_order = data['turn_order']
  socket_ids = data['socket_ids']
  client_user_turn = false

  
  for(let x = 0; x<socket_ids;x++){
  }
  players_info_list = data['player_info'];
  for(let i =1; i<players_info_list.length;i++){
    document.getElementById(`ready_mark${i}`).style.display = ''
  }

  other_player_listw_dealer = players_info_list.map(obj => ({ ...obj }));
    players_amount = data['player_list_length'];
    // if the only player is the main client then there is no need to display others
    if(players_amount==1){

      document.getElementById(`other_profile2`).style.display = 'none';
      document.getElementById(`player2-cards`).style.display = 'none';
      document.getElementById(`player2-profilepic`).style.display = 'none';
      document.getElementById(`player2-username`).style.display = 'none';
      document.getElementById(`player2-balance`).style.display = 'none';
      document.getElementById(`player2-cards`).style.display = 'none';
      document.getElementById(`player2-currentbet`).style.display= 'none';


      document.getElementById(`other_profile3`).style.display = 'none';
      document.getElementById(`player3-cards`).style.display = 'none';
      document.getElementById(`player3-profilepic`).style.display = 'none';
      document.getElementById(`player3-username`).style.display = 'none';
      document.getElementById(`player3-balance`).style.display = 'none';
      document.getElementById(`player3-cards`).style.display = 'none';
      document.getElementById(`player3-currentbet`).style.display = 'none';

      document.getElementById(`other_profile4`).style.display = 'none';
      document.getElementById(`player4-cards`).style.display = 'none';
      document.getElementById(`player4-profilepic`).style.display = 'none';
      document.getElementById(`player4-username`).style.display = 'none';
      document.getElementById(`player4-balance`).style.display = 'none';
      document.getElementById(`player4-cards`).style.display = 'none';
      document.getElementById(`player4-currentbet`).style.display = 'none';

      document.getElementById(`other_profile5`).style.display = 'none';
      document.getElementById(`player5-cards`).style.display = 'none';
      document.getElementById(`player5-profilepic`).style.display = 'none';
      document.getElementById(`player5-username`).style.display = 'none';
      document.getElementById(`player5-balance`).style.display = 'none';
      document.getElementById(`player5-cards`).style.display = 'none';
      document.getElementById(`player5-currentbet`).style.display = 'none';
      
    }
    else if(players_amount==2){
      document.getElementById(`other_profile2`).style.display = '';
      document.getElementById(`player2-cards`).style.display = '';
      document.getElementById(`player2-profilepic`).style.display = '';
      document.getElementById(`player2-username`).style.display = '';
      document.getElementById(`player2-balance`).style.display = '';
      document.getElementById(`player2-cards`).style.display = '';
      document.getElementById(`player2-currentbet`).style.display= '';
      //turn displays off
      document.getElementById(`other_profile3`).style.display = 'none';
      document.getElementById(`player3-cards`).style.display = 'none';
      document.getElementById(`player3-profilepic`).style.display = 'none';
      document.getElementById(`player3-username`).style.display = 'none';
      document.getElementById(`player3-balance`).style.display = 'none';
      document.getElementById(`player3-cards`).style.display = 'none';
      document.getElementById(`player3-currentbet`).style.display = 'none';

      document.getElementById(`other_profile4`).style.display = 'none';
      document.getElementById(`player4-cards`).style.display = 'none';
      document.getElementById(`player4-profilepic`).style.display = 'none';
      document.getElementById(`player4-username`).style.display = 'none';
      document.getElementById(`player4-balance`).style.display = 'none';
      document.getElementById(`player4-cards`).style.display = 'none';
      document.getElementById(`player4-currentbet`).style.display = 'none';

      document.getElementById(`other_profile5`).style.display = 'none';
      document.getElementById(`player5-cards`).style.display = 'none';
      document.getElementById(`player5-profilepic`).style.display = 'none';
      document.getElementById(`player5-username`).style.display = 'none';
      document.getElementById(`player5-balance`).style.display = 'none';
      document.getElementById(`player5-cards`).style.display = 'none';
      document.getElementById(`player5-currentbet`).style.display = 'none';


    }else if (players_amount==3){
      document.getElementById(`other_profile2`).style.display = '';
      document.getElementById(`player2-cards`).style.display = '';
      document.getElementById(`player2-profilepic`).style.display = '';
      document.getElementById(`player2-username`).style.display = '';
      document.getElementById(`player2-balance`).style.display = '';
      document.getElementById(`player2-cards`).style.display = '';
      document.getElementById(`player2-currentbet`).style.display = '';

      document.getElementById(`other_profile3`).style.display = '';
      document.getElementById(`player3-cards`).style.display = '';
      document.getElementById(`player3-profilepic`).style.display = '';
      document.getElementById(`player3-username`).style.display = '';
      document.getElementById(`player3-balance`).style.display = '';
      document.getElementById(`player3-cards`).style.display = '';
      document.getElementById(`player3-currentbet`).style.display = '';

      document.getElementById(`other_profile4`).style.display = 'none';
      document.getElementById(`player4-cards`).style.display = 'none';
      document.getElementById(`player4-profilepic`).style.display = 'none';
      document.getElementById(`player4-username`).style.display = 'none';
      document.getElementById(`player4-balance`).style.display = 'none';
      document.getElementById(`player4-cards`).style.display = 'none';
      document.getElementById(`player4-currentbet`).style.display = 'none';

      document.getElementById(`other_profile5`).style.display = 'none';
      document.getElementById(`player5-cards`).style.display = 'none';
      document.getElementById(`player5-profilepic`).style.display = 'none';
      document.getElementById(`player5-username`).style.display = 'none';
      document.getElementById(`player5-balance`).style.display = 'none';
      document.getElementById(`player5-cards`).style.display = 'none';
      document.getElementById(`player5-currentbet`).style.display = 'none';
      
  
    }else if (players_amount==4){
      document.getElementById(`other_profile2`).style.display = '';
      document.getElementById(`player2-cards`).style.display = '';
      document.getElementById(`player2-profilepic`).style.display = '';
      document.getElementById(`player2-username`).style.display = '';
      document.getElementById(`player2-balance`).style.display = '';
      document.getElementById(`player2-cards`).style.display = '';
      document.getElementById(`player2-currentbet`).style.display = '';
      
      document.getElementById(`other_profile3`).style.display = '';
      document.getElementById(`player3-cards`).style.display = '';
      document.getElementById(`player3-profilepic`).style.display = '';
      document.getElementById(`player3-username`).style.display = '';
      document.getElementById(`player3-balance`).style.display = '';
      document.getElementById(`player3-cards`).style.display = '';
      document.getElementById(`player3-currentbet`).style.display = '';


      document.getElementById(`other_profile4`).style.display = '';
      document.getElementById(`player4-cards`).style.display = '';
      document.getElementById(`player4-profilepic`).style.display = '';
      document.getElementById(`player4-username`).style.display = '';
      document.getElementById(`player4-balance`).style.display = '';
      document.getElementById(`player4-cards`).style.display = '';
      document.getElementById(`player4-currentbet`).style.display = '';

      document.getElementById(`other_profile5`).style.display = 'none';
      document.getElementById(`player5-cards`).style.display = 'none';
      document.getElementById(`player5-profilepic`).style.display = 'none';
      document.getElementById(`player5-username`).style.display = 'none';
      document.getElementById(`player5-balance`).style.display = 'none';
      document.getElementById(`player5-cards`).style.display = 'none';
      document.getElementById(`player5-currentbet`).style.display = 'none';
  
    }
    else if (players_amount==5){
      
      document.getElementById(`other_profile2`).style.display = '';
      document.getElementById(`player2-cards`).style.display = '';
      document.getElementById(`player2-profilepic`).style.display = '';
      document.getElementById(`player2-username`).style.display = '';
      document.getElementById(`player2-balance`).style.display = '';
      document.getElementById(`player2-cards`).style.display = '';
      document.getElementById(`player2-currentbet`).style.display = '';
      
      document.getElementById(`other_profile3`).style.display = '';
      document.getElementById(`player3-cards`).style.display = '';
      document.getElementById(`player3-profilepic`).style.display = '';
      document.getElementById(`player3-username`).style.display = '';
      document.getElementById(`player3-balance`).style.display = '';
      document.getElementById(`player3-cards`).style.display = '';
      document.getElementById(`player3-currentbet`).style.display = '';


      document.getElementById(`other_profile4`).style.display = '';
      document.getElementById(`player4-cards`).style.display = '';
      document.getElementById(`player4-profilepic`).style.display = '';
      document.getElementById(`player4-username`).style.display = '';
      document.getElementById(`player4-balance`).style.display = '';
      document.getElementById(`player4-cards`).style.display = '';
      document.getElementById(`player4-currentbet`).style.display = '';


      document.getElementById(`other_profile5`).style.display = '';
      document.getElementById(`player5-cards`).style.display = '';
      document.getElementById(`player5-profilepic`).style.display = '';
      document.getElementById(`player5-username`).style.display = '';
      document.getElementById(`player5-balance`).style.display = '';
      document.getElementById(`player5-cards`).style.display = '';
      document.getElementById(`player5-currentbet`).style.display = '';
    }
    
    for(let i = 0; i<=players_info_list.length; i++){// to update player 1
      
    if(players_info_list[i]['user_id'] == playerid){
      client_player = players_info_list[i]
      //update the balance of the client's player
      
    document.getElementById(`player1-balance`).innerText = `Balance: ${players_info_list[i][`balance`]}`;
    document.getElementById(`player1-currentbet`).innerText = `Current Bet: ${players_info_list[i][`current_bet`]}`
    //check to see if there is a round in progress
    if(data['all_ready'] == true){
      if(client_player['player_turn']!=true){
        
        socket.emit('removeUI', {'room':roomCode, 'playerid':playerid, 'socket_id':socket.id})
        
        document.getElementById('ready_mark1').style.visibility = 'hidden';
        document.getElementById('ready_mark1').src = '/blackjack/static/checkmark.png?' + new Date().getTime()

        
      }else{
        
        
        socket.emit('createUI',{'room':roomCode, 'playerid':playerid, 'socket_id':socket.id})
        
        document.getElementById('ready_mark1').style.visibility = '';
        document.getElementById('ready_mark1').style.display = '';
        
        
        document.getElementById('ready_mark1').src = '/blackjack/static/mario_star.png?' + new Date().getTime()
      }
        if(client_player['hand'].length!=0){
          
          
          

          if(client_player['hand'].length - document.getElementById('player').querySelectorAll('img').length ==1){
            
            card = document.createElement('img');
            
            card.src ='/blackjack/static/'+client_player['hand'][client_player['hand'].length-1]['image'];
            
            document.getElementById(`player`).appendChild(card)
            
            
            
          }else if(players_info_list[i]['hand'].length - document.getElementById('player').querySelectorAll('img').length >=2){
            
            for(let h =0; h<players_info_list[i]['hand'].length;h++ ){
              
              card = document.createElement('img');
              card.src ='/blackjack/static/'+client_player['hand'][h]['image']
              document.getElementById(`player`).appendChild(card)
          }
          }
        }
         if(client_player['player_bust'] == true){
          
           document.getElementById('result-message1').style.visibility = ''
           document.getElementById('hit-button').disabled = true
           document.getElementById('stand-button').disabled = true
           document.getElementById('double-button').disabled = true
         }else{
           
           document.getElementById('result-message1').style.visibility = 'hidden'
           document.getElementById('hit-button').disabled = false
           document.getElementById('stand-button').disabled = false
           document.getElementById('double-button').disabled = false

         }
    document.getElementById('bet-amount').style.display = 'none'
    document.getElementById('place-bet-button').style.display = 'none'

    }else{
      document.getElementById('place-bet-button').disabled = false;
      document.getElementById('place-bet-button').style.display = '';
      document.getElementById('bet-amount').style.display = ''
      document.getElementById('stand-button').style.display = 'none';
      document.getElementById('hit-button').style.display = 'none';
      document.getElementById('double-button').style.display = 'none';

      //document.getElementById('stand-button').disabled = true;
      //document.getElementById('hit-button').disabled = true;
      //document.getElementById('double-button').disabled = true;
        if(client_player['player_status'] =='ready'){
          ready_mark = document.getElementById('ready_mark1')
          ready_mark.style.display = ''
          ready_mark.style.visibility = 'visibile'
          ready_mark.src = '/blackjack/static/checkmark.png?'+ new Date().getTime()
          
        }else{
          ready_mark = document.getElementById('ready_mark1')
          ready_mark.style.display = ''
          ready_mark.style.visibility = 'visible'
          ready_mark.src = src="/blackjack/static/xmark.png"

        }
      
    }
      other_player_listw_dealer.splice(i,1)
     //players_info_list.splice(i,1); 
     break;
  }
    }
      for(let i = 1; i<other_player_listw_dealer.length; i++){ 
        //populate the other players name and balance
        document.getElementById(`player${i+1}-username`).innerText = `Username:${other_player_listw_dealer[i]['username']}`;
        
        document.getElementById(`player${i+1}-balance`).innerText = `Balance:${other_player_listw_dealer[i]['balance']}`;
        document.getElementById(`player${i+1}-currentbet`).innerText = `Current Bet: ${other_player_listw_dealer[i]['current_bet']}`
        //if the round hasn't started, display who is ready to begin round
        if(data['all_ready']==false){
          if(other_player_listw_dealer[i]['player_status'] == 'ready'){
          ready_status = document.getElementById(`ready_mark${i+1}`);
          ready_status.src = '/blackjack/static/checkmark.png?'+new Date().getTime();
          ready_status.style.display = '';
          ready_status.style.visibility = 'visible'
        }else{
          ready_status = document.getElementById(`ready_mark${i+1}`);
          ready_status.src = "/blackjack/static/xmark.png"
          ready_status.style.display = '';
          ready_status.style.visibility = 'visible'
        }
      }
      else{
          if(client_player['player_turn'] == false){
            
            for(let x =1; x<other_player_listw_dealer.length;x++){
              
              if(other_player_listw_dealer[i]['player_turn']==true){
                ready_status = document.getElementById(`ready_mark${i+1}`);
                ready_status.style.visibility = ''
                ready_status.src = '/blackjack/static/mario_star.png?'+ new Date().getTime()
                break
      
              }else{
                ready_status = document.getElementById(`ready_mark${i+1}`);
                ready_status.style.visibility = 'hidden'
                ready_status.src = '/blackjack/static/checkmark.png?'+ new Date().getTime()
              }
            }
          }else{
            document.getElementById(`ready_mark${i+1}`).style.visibility = 'hidden'
  
          }
          
          
          for(let i =1; i<other_player_listw_dealer.length;i++){
            
            if(other_player_listw_dealer[i]['result']!=''){ document.getElementById(`result-message${i+1}`).style.visibility = ''}
            if(other_player_listw_dealer[i]['player_bust']==true){ document.getElementById(`result-message${i+1}`).style.visibility = ''}

              if(other_player_listw_dealer[i]['hand'].length - document.getElementById(`player${i+1}-cards`).querySelectorAll('img').length ==1){
                card = document.createElement('img');
                card.src ='/blackjack/static/'+other_player_listw_dealer[1]['hand'][other_player_listw_dealer[i]['hand'].length-1]['image'];
                
                document.getElementById(`player${i+1}-cards`).appendChild(card)
              }else if(other_player_listw_dealer[i]['hand'].length - document.getElementById(`player${i+1}-cards`).querySelectorAll('img').length >=2){
                for(let h =0; h<other_player_listw_dealer[i]['hand'].length;h++ ){
                  
                  card = document.createElement('img');
                  card.src ='/blackjack/static/'+other_player_listw_dealer[i]['hand'][h]['image'];
                  document.getElementById(`player${i+1}-cards`).appendChild(card)
              }
              }
  
            
          }
        }
      }

    
   
      


    //show dealers hand if round is in progress
    if(data['all_ready']==true){
      document.getElementById('dealer').style.display = ''
    if(players_info_list[0]['hand'].length!=0){
      console.log('in dealer hand')
      
        if(players_info_list[0]['hand'].length - document.getElementById(`dealer`).querySelectorAll('img').length ==1){
        card = document.createElement('img');
        card.src = '/blackjack/static/' + players_info_list[0]['hand'][players_info_list[0]['hand'].length-1]['image'];
        document.getElementById(`dealer`).appendChild(card);
      }
      else if(players_info_list[0]['hand'].length - document.getElementById(`dealer`).querySelectorAll('img').length >=2){
        let dealer_cards = document.getElementById('dealer').querySelectorAll('img')
        dealer_cards.forEach(card=>{
          card.remove()
        });
        console.log('in dealer else if')
        for(let h =0; h<players_info_list[0]['hand'].length; h++){
        card = document.createElement('img');
        card.src = '/blackjack/static/' + players_info_list[0]['hand'][h]['image'];
        document.getElementById(`dealer`).appendChild(card);
      }
      }
    }
      
    }
    
    if(players_info_list[0]['player_turn'] == true && client_player['is_last']==true ){
      socket.emit('dealer_play', {'room':roomCode, 'player_info':players_info_list, 'playerid':playerid})
      }


  }); 

socket.on('update_balance_results', async function(data){
  console.log('IN UPDATE BALANCE RESULTS')
  let players = data['players_data']
   document.getElementById('dealer').querySelectorAll('img').forEach(o=>{
     o.remove();
   });

  // for(let i =0;i<players_info_list[0]['hand'].length;i++){
  //   let mouse = document.createElement('img');
  //       mouse.src = '/static/' + players_info_list[0]['hand'][i]['image'];
  //       document.getElementById(`dealer`).appendChild(mouse);
  // }
  
  console.log('emitting update_endgame')
  socket.emit('update_endgame', {'room':roomCode, 'player_info':players,'player_list_length':data['player_list_length'], 'all_ready':data['all_ready'],'turn_order': data['turn_order'], })
  console.log('emitted upate_endgame')
  

  //HUGE BLOCK INCOMING
  //
  //
  





  // HUGE BLOCK END
  //
  //
  console.log('result:'+client_player['result'])
  await new Promise(resolve => setTimeout(resolve, 500));

if(client_player['result'] =='bust'){
    console.log('in bust')
    document.getElementById('result-message1').innerText = 'BUST!'
    document.getElementById('result-message1').style.visibility = 'visible'
    

  }else if(client_player['result']=='winner'){
    document.getElementById('result-message1').innerText = 'WINNER!'
    document.getElementById('result-message1').style.visibility = 'visible'
    console.log('in winner')
  }else if(client_player['result']== 'blackjack'){
    console.log('in blackjack')
    document.getElementById('result-message1').innerText = 'BLACKJACK!'
    document.getElementById('result-message1').style.visibility = 'visible'
    

  }else if(client_player['result']== 'loser'){
    console.log('in loser')
    document.getElementById('result-message1').innerText = 'LOSER!'
    document.getElementById('result-message1').style.visibility = 'visible'
  }else if(client_player['result']== 'push'){
    console.log('in in push')
    document.getElementById('result-message1').innerText = 'PUSH!'
    document.getElementById('result-message1').style.visibility = 'visible'
  }
  console.log('for loop length'+other_player_listw_dealer.length)
  for(let x =1;x<other_player_listw_dealer.length-1;x++){
    console.log('IN OTHER FOR LOOP')
    if(other_player_listw_dealer[x]['result'] == 'bust'){

    document.getElementById(`result-message${x+1}`).innerText = 'BUST!'
    document.getElementById(`result-message${x+1}`).style.visibility = 'visible'

    }else if(other_player_listw_dealer[x]['result']== 'winner'){
      document.getElementById(`result-message${x+1}`).innerText = 'WINNER!'
      document.getElementById(`result-message${x+1}`).style.visibility = 'visible'
    }else if(other_player_listw_dealer[x]['result']== 'blackjack'){
      document.getElementById(`result-message${x+1}`).innerText = 'BLACKJACK!'
      document.getElementById(`result-message${x+1}`).style.visibility = 'visible'
    }else if(other_player_listw_dealer[x]['result'] == 'loser'){
      document.getElementById(`result-message${x+1}`).innerText = 'LOSER!'
      document.getElementById(`result-message${x+1}`).style.visibility = 'visible'
    }else if(other_player_listw_dealer[x]['result'] == 'push'){
      document.getElementById(`result-message${x+1}`).innerText = 'PUSH!'
      document.getElementById(`result-message${x+1}`).style.visibility = 'visible'
    }
  }
  
  console.log('calling end_round')
  await new Promise(resolve => setTimeout(resolve, 3000));
  
  //remove result screens
  for(let x=1; x<6;x++){
    document.getElementById(`result-message${x}`).style.visibility ='hidden'
  }
  // Select the div by its id
let player1_cards = document.getElementById('player').querySelectorAll('img')
let player2_cards = document.getElementById('player2-cards').querySelectorAll('img')
let player3_cards = document.getElementById('player3-cards').querySelectorAll('img')
let player4_cards = document.getElementById('player4-cards').querySelectorAll('img')
let player5_cards = document.getElementById('player5-cards').querySelectorAll('img')
let dealer_cards = document.getElementById('dealer').querySelectorAll('img')

//remove images from each hand
player1_cards.forEach(card =>{
  card.remove();
});
player2_cards.forEach(card =>{
  card.remove();
});
player3_cards.forEach(card =>{
  card.remove();
});
player4_cards.forEach(card =>{
  card.remove();
});
player5_cards.forEach(card =>{
  card.remove();
});
dealer_cards.forEach(card =>{
  card.remove();
});
    console.log('emitting end round')
    socket.emit('end_round', {'room':roomCode})

})
  
    
document.getElementById('place-bet-button').addEventListener('click',function(){
   value = document.getElementById('bet-amount').value
   socket.emit('place_bet', {'value':value, 'room':roomCode, 'playerid':playerid})

 });



 document.getElementById('hit-button').addEventListener('click', function(){
  socket.emit('hit_event', {'room':roomCode, 'playerid':playerid})
 });

 document.getElementById('stand-button').addEventListener('click',function(){
  socket.emit('stand_event', {'room':roomCode, 'playerid':playerid})

});
document.getElementById('double-button').addEventListener('click',function(){
  socket.emit('double_event', {'room':roomCode, 'playerid':playerid})

});


socket.on('hit-event-client',function(data){
  room = data['room']
  let player_data = data['player_info']
  let round_over = data['round_over']
  
  socket.emit('call_server', {'all_ready':data['all_ready'],'room':room, 'player_bust':data['player_bust'],'player_info':player_data,'round_over':round_over, 'turn_order':data['turn_order'], 'player_list_length':data['player_list_length']})
  
  

});




socket.on('createUI',function(data){
  document.getElementById('hit-button').style.display = ''
  document.getElementById('hit-button').offsetHeight
  document.getElementById('stand-button').style.display= ''
  document.getElementById('stand-button').offsetHeight
  if(client_player['hand'].length == 2){
  document.getElementById('double-button').style.display= ''
  document.getElementById('double-button').offsetHeight
  }else{
  document.getElementById('double-button').style.display= 'none'
  document.getElementById('double-button').offsetHeight
  }
  
 });

socket.on('removeUI',function(data){
  
  document.getElementById('hit-button').style.display= 'none'
  document.getElementById('hit-button').offsetHeight
  document.getElementById('stand-button').style.display= 'none'
  document.getElementById('stand-button').offsetHeight
  document.getElementById('double-button').style.display= 'none'
  document.getElementById('double-button').offsetHeight

 });


document.getElementById('leave-button').addEventListener('click', function(){
  socket.disconnect()
  window.location.href = `/title.html`
})
socket.on('error',function(data){
  message = data['message']
  alert(message)

});

document.getElementById('send-button').addEventListener('click',function(){
  const input = document.getElementById('message-input');
    const message = input.value.trim();

    if (message !== '') {
        const username = `${client_player['username']}`; // Replace with dynamic username if needed
        const fullMessage = `${username}: ${message}`;

        // Emit the 'chat_event' with the message to the server
        socket.emit('chat_event', {'message':fullMessage,'room':roomCode});

        // Clear the input field after sending
        input.value = '';
    }
});
socket.on('update_chat',function(data){
  const chatMessages = document.getElementById('chat-messages');

    // Create the message div and add the class
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message');
    messageDiv.textContent = data.message;

    // Append the new message
    chatMessages.appendChild(messageDiv);

    // Ensure we scroll to the bottom
    requestAnimationFrame(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    // Keep chat messages at a limit (e.g., 50 messages)
    const maxMessages = 50;
    if (chatMessages.children.length > maxMessages) {
        chatMessages.removeChild(chatMessages.firstChild);
    }
})
document.getElementById('message-input').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
      document.getElementById('send-button').click();
  }
});

