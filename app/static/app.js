//const TYPING_SPEED = 20;
//
//function createAssistantDiv(chatBoxId) {
//  const div = document.createElement("div");
//  div.className = "message assistant";
//  document.getElementById(chatBoxId).appendChild(div);
//  return div;
//}
//
//function addUserMessage(chatBoxId, text) {
//  const div = document.createElement("div");
//  div.className = "message user";
//  div.textContent = text;
//  document.getElementById(chatBoxId).appendChild(div);
//}
//
///* =========================================================
//   WEBSOCKET CHAT
//========================================================= */
//
//let ws;
//let wsAssistantDiv = null;
//let wsBuffer = "";
//let wsTyping = false;
//
//function initWebSocket() {
//  const protocol = location.protocol === "https:" ? "wss" : "ws";
//  ws = new WebSocket(`${protocol}://${location.host}/chat/ws`);
//
//  ws.onmessage = e => {
//    if (!wsAssistantDiv) {
//      wsAssistantDiv = createAssistantDiv("chatBoxWS");
//    }
//    wsBuffer += e.data;
//    if (!wsTyping) typeWS();
//  };
//
//  ws.onclose = () => setTimeout(initWebSocket, 2000);
//}
//
//function typeWS() {
//  if (wsBuffer.length > 0) {
//    wsTyping = true;
//    wsAssistantDiv.textContent += wsBuffer[0];
//    wsBuffer = wsBuffer.slice(1);
//    setTimeout(typeWS, TYPING_SPEED);
//  } else {
//    wsTyping = false;
//  }
//}
//
//function sendMessageWS() {
//  const input = document.getElementById("messageInputWS");
//  const msg = input.value.trim();
//  if (!msg || ws.readyState !== WebSocket.OPEN) return;
//
//  addUserMessage("chatBoxWS", msg);
//  input.value = "";
//
//  wsAssistantDiv = null;
//  wsBuffer = "";
//  wsTyping = false;
//
//  ws.send(msg);
//}
//
//function handleEnterWS(e) {
//  if (e.key === "Enter") sendMessageWS();
//}
//
///* =========================================================
//   SOCKET.IO CHAT (FIXED)
//========================================================= */
//
//let ioSocket;
//let ioAssistantDiv = null;
//let ioBuffer = "";
//let ioTyping = false;
//
//function initSocketIO() {
//ioSocket = io({
//  transports: ["websocket"]
//});
//
//
//  ioSocket.on("connect", () => {
//    console.log("Socket.IO connected");
//  });
//
//  ioSocket.on("chat_token", token => {
//    if (!ioAssistantDiv) {
//      ioAssistantDiv = createAssistantDiv("chatBoxIO");
//    }
//    ioBuffer += token;
//    if (!ioTyping) typeIO();
//  });
//
//  ioSocket.on("chat_complete", () => {
//    ioAssistantDiv = null;
//  });
//}
//
//function typeIO() {
//  if (ioBuffer.length > 0) {
//    ioTyping = true;
//    ioAssistantDiv.textContent += ioBuffer[0];
//    ioBuffer = ioBuffer.slice(1);
//    setTimeout(typeIO, TYPING_SPEED);
//  } else {
//    ioTyping = false;
//  }
//}
//
//function sendMessageIO() {
//  const input = document.getElementById("messageInputIO");
//  const msg = input.value.trim();
//  if (!msg || !ioSocket?.connected) return;
//
//  addUserMessage("chatBoxIO", msg);
//  input.value = "";
//
//  ioAssistantDiv = null;
//  ioBuffer = "";
//  ioTyping = false;
//
//  ioSocket.emit("chat_message", { question: msg });
//}
//
//function handleEnterIO(e) {
//  if (e.key === "Enter") sendMessageIO();
//}
//
///* =========================================================
//   DOCUMENT UPLOAD
//========================================================= */
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
//    const res = await fetch("/upload/", { method: "POST", body: formData });
//    const data = await res.json();
//    status.textContent = data.message;
//  } catch {
//    status.textContent = "Upload failed";
//  }
//}
//
///* =========================================================
//   INIT
//========================================================= */
//
//window.onload = () => {
//  initWebSocket();
//  initSocketIO();
//};
//
