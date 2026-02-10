//let socket;
//let assistantDiv = null;
//
//function initWebSocket() {
//  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
//  const wsUrl = `${protocol}://${window.location.host}/chat/ws`;
//
//  socket = new WebSocket(wsUrl);
//
//  socket.onopen = () => {
//    console.log("WebSocket connected");
//  };
//
//  socket.onmessage = (event) => {
//    if (!assistantDiv) {
//      assistantDiv = document.createElement("div");
//      assistantDiv.classList.add("message", "assistant");
//      document.getElementById("chatBox").appendChild(assistantDiv);
//    }
//
//    assistantDiv.textContent += event.data;
//    document.getElementById("chatBox").scrollTop =
//      document.getElementById("chatBox").scrollHeight;
//  };
//
//  socket.onerror = (err) => {
//    console.error("WebSocket error", err);
//  };
//
//  socket.onclose = () => {
//    console.warn("WebSocket closed. Reconnecting...");
//    setTimeout(initWebSocket, 2000);
//  };
//}
//
//function addMessage(text, sender) {
//  const chatBox = document.getElementById("chatBox");
//  const div = document.createElement("div");
//  div.classList.add("message", sender);
//  div.textContent = text;
//  chatBox.appendChild(div);
//  chatBox.scrollTop = chatBox.scrollHeight;
//}
//
//function sendMessage() {
//  if (!socket || socket.readyState !== WebSocket.OPEN) {
//    alert("WebSocket not connected");
//    return;
//  }
//
//  const input = document.getElementById("messageInput");
//  const message = input.value.trim();
//  if (!message) return;
//
//  addMessage(message, "user");
//  input.value = "";
//
//  assistantDiv = null;
//  socket.send(message);
//}
//
//function handleEnter(event) {
//  if (event.key === "Enter") {
//    sendMessage();
//  }
//}
//
//async function uploadDocument() {
//  const fileInput = document.getElementById("fileInput");
//  const status = document.getElementById("uploadStatus");
//
//  if (!fileInput.files.length) {
//    status.textContent = "Please select a file";
//    return;
//  }
//
//  const formData = new FormData();
//  formData.append("file", fileInput.files[0]);
//
//  try {
//    const res = await fetch("/upload/", {
//      method: "POST",
//      body: formData
//    });
//
//    const data = await res.json();
//    status.textContent = data.message;
//  } catch (err) {
//    console.error(err);
//    status.textContent = "Upload failed";
//  }
//}
//
//window.onload = initWebSocket;


let socket;
let assistantDiv = null;

// 🔹 Typing effect controls
let textBuffer = "";
let isTyping = false;
const TYPING_SPEED = 20; // ⏱ Change this (ms). Lower = faster

function initWebSocket() {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const wsUrl = `${protocol}://${window.location.host}/chat/ws`;

  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onmessage = (event) => {
    if (!assistantDiv) {
      assistantDiv = document.createElement("div");
      assistantDiv.classList.add("message", "assistant");
      document.getElementById("chatBox").appendChild(assistantDiv);
    }

    // Add incoming text to buffer instead of showing immediately
    textBuffer += event.data;

    if (!isTyping) {
      typeWriter();
    }
  };

  socket.onerror = (err) => {
    console.error("WebSocket error", err);
  };

  socket.onclose = () => {
    console.warn("WebSocket closed. Reconnecting...");
    setTimeout(initWebSocket, 2000);
  };
}

// 🔹 Typing animation function
function typeWriter() {
  if (textBuffer.length > 0) {
    isTyping = true;

    assistantDiv.textContent += textBuffer[0];
    textBuffer = textBuffer.slice(1);

    document.getElementById("chatBox").scrollTop =
      document.getElementById("chatBox").scrollHeight;

    setTimeout(typeWriter, TYPING_SPEED);
  } else {
    isTyping = false;
  }
}

function addMessage(text, sender) {
  const chatBox = document.getElementById("chatBox");
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    alert("WebSocket not connected");
    return;
  }

  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  assistantDiv = null;
  textBuffer = "";   // reset buffer for new response
  isTyping = false;

  socket.send(message);
}

function handleEnter(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

async function uploadDocument() {
  const fileInput = document.getElementById("fileInput");
  const status = document.getElementById("uploadStatus");

  if (!fileInput.files.length) {
    status.textContent = "Please select a file";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const res = await fetch("/upload/", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    status.textContent = data.message;
  } catch (err) {
    console.error(err);
    status.textContent = "Upload failed";
  }
}

window.onload = initWebSocket;
