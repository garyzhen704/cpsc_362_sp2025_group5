
// Assuming you are using 
// socket.io, initialize the socket connection here
const socket = io('/title');


document.addEventListener("DOMContentLoaded", function() {
  console.log("DOM fully loaded and parsed!");
  const hostButton = document.getElementById("host_button");
  const joinButton = document.getElementById("join_button");
  const joinCodeButton = document.getElementById("join_code_button");
 // Get references to buttons
 console.log(hostButton, joinButton, joinCodeButton); 


     // Event listener for 'Host a Game' button
// Event listener for 'Host a Game' button
hostButton.addEventListener("click", function() {
  const username = prompt("Enter your username:");
  console.log(`Host button clicked. Username entered: ${username}`);
        if (username) {
            console.log(`Hosting game for: ${username}`);  // To check the username
            // Emit event to server to create a game
            socket.emit('host', { username: username });
        } else {
            alert("Username is required to host a game.");
        }
    });

// Event listener for 'Join a Game' button
joinButton.addEventListener("click", function() {
  const username = prompt("Enter your username:");
  if (username) {
      socket.emit('join', { username: username });
  } else {
      alert("Username is required to join a game.");
  }
});

// Event listener for 'Enter Join Code' button
joinCodeButton.addEventListener("click", function() {
  const username = prompt("Enter your username:");
  const roomCode = prompt("Enter the room code:");
  if (username && roomCode) {
      socket.emit('join_with_id', { username: username, room: roomCode });
  } else {
      alert("Both username and room code are required.");
  }
});

socket.on('render_game',function(data){
    console.log('rendering')
    room = data['room']
    username = data['username']
    window.location.href = `/game.html?room=${room}&username=${username}&playerid=${data['player_id']}`;


});

socket.on('no_space',function(){
    alert("No rooms left to host.");
});

socket.on('error',function(data){
    alert(data['message'])
});

});


