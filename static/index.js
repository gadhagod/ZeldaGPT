var socket = io();

socket.on("connect", () => {
    let askBtn = document.getElementById("ask");
    let questionBox = document.getElementById("question");
    let answerContainer = document.getElementById("answer-container");
    let thinkingMsg = document.getElementById("thinking");
    let responseBox = document.getElementById("response");

    let ask = () => {
        let question = document.getElementById("question").value;
        socket.send(question);
        thinkingMsg.classList.remove("hidden");
        responseBox.classList.add("hidden");
        answerContainer.classList.remove("hidden");
    };

    let answer = (response) => {
        responseBox.innerText = response;
        thinkingMsg.classList.add("hidden");
        responseBox.classList.remove("hidden");
    };


    questionBox.addEventListener("input", () => {
        if (questionBox.value) {
            askBtn.removeAttribute("disabled")
        } else {
            askBtn.setAttribute("disabled", "")
        }
    });

    questionBox.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            ask();
        }
  });

    askBtn.addEventListener("click", ask);
    
    socket.on("message", answer);

    console.log("Connected!");
});

var ellipses = document.getElementById("ellipses");

setInterval(() => {
    if (ellipses.innerText.length == 2) {
        ellipses.innerText = "";
    } else {
        ellipses.innerText += ".";
    }
}, 1000);