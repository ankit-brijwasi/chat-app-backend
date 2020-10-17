const roomName = getRoomName();
const currentUser = getCurrentUser();

const messagesContainer = document.getElementById("messages");
if (messagesContainer.scrollHeight > 400) {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

const chatSocket = new ReconnectingWebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);

chatSocket.onmessage = function (e) {
  const response = JSON.parse(e.data);
  const msgBox = document.getElementById("messages");
  const msgContainer = document.createElement("div");
  const recieved = document.createElement("div");
  const p = document.createElement("p");
  const pAuthor = document.createElement("p");
  const date = new Date(response.data.sent_on);

  const months = [
    "Jan.",
    "Feb.",
    "Mar.",
    "Apr.",
    "May",
    "Jun.",
    "Jul.",
    "Aug.",
    "Sep.",
    "Oct.",
    "Nov.",
    "Dec.",
  ];

  const message = document.createTextNode(response.data.message);
  const timeStamp = document.createTextNode(
    months[date.getMonth()] +
      " " +
      date.getDate() +
      ", " +
      date.getHours() +
      ":" +
      date.getSeconds()
  );

  msgContainer.classList.add("flex");
  if (response.data.author.username !== currentUser) {
    pAuthor.classList.add("author");
    pAuthor.appendChild(document.createTextNode(response.data.author.username));
    msgContainer.style.justifyContent = "flex-start";
    recieved.classList.add("message-recieved");
    recieved.appendChild(pAuthor);
  } else {
    msgContainer.style.justifyContent = "flex-end";
    recieved.classList.add("message-sent");
  }

  p.classList.add("time");

  p.appendChild(timeStamp);
  recieved.appendChild(message);
  recieved.appendChild(p);
  msgContainer.appendChild(recieved);
  msgBox.appendChild(msgContainer);
  if (msgBox.scrollHeight > 400) {
    msgBox.scrollTop = msgBox.scrollHeight;
  }
};

chatSocket.onclose = function (e) {
  console.warn("Chat socket closed unexpectedly");
};

// document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-input").onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter, return
    document.querySelector("#chat-message-submit").click();
  }
};

document.querySelector("#chat-message-submit").onclick = function (e) {
  const messageInputDom = document.querySelector("#chat-message-input");
  const message = messageInputDom.value;
  chatSocket.send(
    JSON.stringify({
      message: message,
    })
  );
  messageInputDom.value = "";
};
