let socket;
let assistantDiv = null;

let textBuffer = "";
let isTyping = false;
const TYPING_SPEED = 20;

function initSocket() {
  socket = io(window.location.origin, {
    path: "/socket.io",
    transports: ["websocket"]
  });

  socket.on("connect", () => {
    console.log("Connected to server");
  });

  socket.on("chat_token", (token) => {
    if (!assistantDiv) {
      assistantDiv = document.createElement("div");
      assistantDiv.classList.add("message", "assistant");
      document.getElementById("chatBox").appendChild(assistantDiv);
    }

    textBuffer += token;

    if (!isTyping) typeWriter();
  });

  socket.on("chat_complete", () => {
    console.log("Response complete");
  });
}

function typeWriter() {
  if (textBuffer.length > 0) {
    isTyping = true;

    assistantDiv.textContent += textBuffer[0];
    textBuffer = textBuffer.slice(1);

    const chatBox = document.getElementById("chatBox");
    chatBox.scrollTop = chatBox.scrollHeight;

    setTimeout(typeWriter, TYPING_SPEED);
  } else {
    isTyping = false;
  }
}

function sendMessage() {
  if (!socket || !socket.connected) {
    alert("Socket not connected");
    return;
  }

  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  assistantDiv = null;
  textBuffer = "";
  isTyping = false;

  socket.emit("chat_message", { question: message });
}

function addMessage(text, sender) {
  const chatBox = document.getElementById("chatBox");
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.textContent = text;
  chatBox.appendChild(div);
}

window.onload = initSocket;
