function toggleChat() {
  const chatbox = document.getElementById("chatbox");
  chatbox.style.display = chatbox.style.display === "flex" ? "none" : "flex";
  chatbox.style.flexDirection = "column";
}

function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (message === "") return;

  const messagesContainer = document.getElementById("messages");
  messagesContainer.innerHTML += `<div><strong>You:</strong> ${message}</div>`;
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  const typingMsg = document.createElement("div");
  typingMsg.innerHTML = "<strong>Bot:</strong> <em>typing...</em>";
  messagesContainer.appendChild(typingMsg);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  setTimeout(() => {
    messagesContainer.removeChild(typingMsg);

    if (message.toLowerCase().includes("weather")) {
      getMumbaiWeather();
    } else {
      let reply = getBotReply(message);
      messagesContainer.innerHTML += `<div><strong>Bot:</strong> ${reply}</div>`;
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }, 600);

  input.value = "";
}

function getBotReply(message) {
  const text = message.toLowerCase();

  if (text.includes("hello") || text.includes("hi")) {
    return "Hello! 👋 How can I help you today?";
  } else if (text.includes("accuracy")) {
    return "Our rainfall prediction model’s accuracy is displayed on the homepage 📊.";
  } else if (text.includes("how to use")) {
    return "Enter Temperature, Humidity, Pressure, and Wind Speed — then click Predict!";
  } else if (text.includes("thank")) {
    return "You're welcome! 🌈";
  } else if (text.includes("help")) {
    return "Ask me about 'current weather', 'accuracy', or how to use the prediction form.";
  } else {
    const replies = [
      "I'm your WeatherBot 🌦️ — ask me for 'current weather'!",
      "Type 'current weather' or 'weather' for Mumbai’s live conditions ☁️.",
      "Need help? Type 'help' 📖."
    ];
    return replies[Math.floor(Math.random() * replies.length)];
  }
}

// 📡 Fetch Mumbai weather (with all 4 stats clearly)
function getMumbaiWeather() {
  const apiKey = 'cdd1d75e4da5755bd42a1342f6a73512'; // Replace this with your OpenWeatherMap API key
  const url = `https://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid=${apiKey}&units=metric`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      const reply = `
        <br>🌡️ <strong>Temperature:</strong> ${data.main.temp}°C
        <br>💧 <strong>Humidity:</strong> ${data.main.humidity}%
        <br>🌀 <strong>Wind Speed:</strong> ${data.wind.speed} m/s
        <br>📈 <strong>Pressure:</strong> ${data.main.pressure} hPa
      `;
      document.getElementById("messages").innerHTML += `<div><strong>Bot:</strong> ${reply}</div>`;
      document.getElementById("messages").scrollTop = document.getElementById("messages").scrollHeight;
    })
    .catch(() => {
      document.getElementById("messages").innerHTML += `<div><strong>Bot:</strong> Sorry — couldn't fetch live weather data 🌧️.</div>`;
    });
}
