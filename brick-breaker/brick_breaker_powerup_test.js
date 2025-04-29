// brick_breaker_powerup_test.js

// This is a white box unit test for the spawnPowerUp function

// Mock the minimum required elements from the original game
const powerUpTypes = ["paddleWidth", "extraBall", "extraLife", "tripleBall"];
let powerUps = [];

// Import the spawnPowerUp function (copied from the original code)
function spawnPowerUp(x, y) { 
  const type = powerUpTypes[Math.floor(Math.random() * powerUpTypes.length)];
  powerUps.push({x: x, y: y, type: type});
}

// White box test for spawnPowerUp
function testSpawnPowerUp() {
  console.log("Starting white box test for spawnPowerUp function");
  
  // Clear any existing power-ups
  powerUps = [];
  
  // Test coordinates
  const testX = 150;
  const testY = 100;
  
  // Test 1: Basic functionality
  spawnPowerUp(testX, testY);
  console.assert(powerUps.length === 1, "Test 1 Failed: Power-up not added to array");
  console.assert(powerUps[0].x === testX, "Test 1 Failed: X position incorrect");
  console.assert(powerUps[0].y === testY, "Test 1 Failed: Y position incorrect");
  console.assert(powerUpTypes.includes(powerUps[0].type), "Test 1 Failed: Invalid power-up type");
  console.log("Test 1 Passed: Basic power-up creation works");
  
  // Test 2: Multiple power-ups
  powerUps = [];
  for (let i = 0; i < 10; i++) {
    spawnPowerUp(testX + i*10, testY + i*5);
  }
  console.assert(powerUps.length === 10, "Test 2 Failed: Not all power-ups created");
  for (let i = 0; i < 10; i++) {
    console.assert(powerUps[i].x === testX + i*10, `Test 2 Failed: Power-up ${i} has incorrect X position`);
    console.assert(powerUps[i].y === testY + i*5, `Test 2 Failed: Power-up ${i} has incorrect Y position`);
  }
  console.log("Test 2 Passed: Multiple power-ups creation works");
  
  // Test 3: Type distribution test
  powerUps = [];
  
  // Mock Math.random to test type selection logic
  const originalRandom = Math.random;
  const mockRandomValues = [0, 0.25, 0.5, 0.75]; // Values to select each type
  let randomIndex = 0;
  
  Math.random = function() {
    return mockRandomValues[randomIndex++ % mockRandomValues.length];
  };
  
  // Create one of each type
  for (let i = 0; i < 4; i++) {
    spawnPowerUp(testX, testY);
  }
  
  // Verify each type was created
  const typeCounts = {};
  powerUpTypes.forEach(type => typeCounts[type] = 0);
  
  powerUps.forEach(pu => typeCounts[pu.type]++);
  
  let allTypesCreated = powerUpTypes.every(type => typeCounts[type] === 1);
  console.assert(allTypesCreated, "Test 3 Failed: Not all power-up types were created");
  console.log("Test 3 Passed: Power-up type selection works");
  
  // Restore original Math.random
  Math.random = originalRandom;
  
  console.log("All spawnPowerUp tests passed!");
}

// Run the test
testSpawnPowerUp();