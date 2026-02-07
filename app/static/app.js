let socket;
let assistantDiv = null;

// Initialize WebSocket
function initWebSocket() {
  socket = new WebSocket(`ws://${window.location.host}/`);

  socket.onmessage = (event) => {
    // Stream tokens into the same assistant bubble
    if (!assistantDiv) {
      assistantDiv = document.createElement("div");
      assistantDiv.classList.add("message", "assistant");
      document.getElementById("chatBox").appendChild(assistantDiv);
    }

    assistantDiv.textContent += event.data;
    document.getElementById("chatBox").scrollTop =
      document.getElementById("chatBox").scrollHeight;
  };

  socket.onclose = () => {
    console.error("WebSocket closed");
  };
}

function addMessage(text, sender) {
  const chatBox = document.getElementById("chatBox");
  const div = document.createElement("div");
  div.classList.add("message", sender);
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message via WebSocket
function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;

  addMessage(message, "user");
  input.value = "";

  assistantDiv = null; // reset assistant bubble
  socket.send(message);
}

function handleEnter(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

// Document upload
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
    const res = await fetch("/documents/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    status.textContent = data.message;
  } catch (err) {
    status.textContent = "Upload failed";
  }
}

window.onload = initWebSocket;
