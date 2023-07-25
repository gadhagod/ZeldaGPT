var socket = io();

socket.on("connect", () => {
    let askBtn = document.getElementById("ask");
    let answerContainer = document.getElementById("answer-container");
    let thinkingMsg = document.getElementById("thinking");
    let responseBox = document.getElementById("response");

    let ask = () => {
        questionBox.setAttribute("disabled", "");
        askBtn.setAttribute("disabled", "");
        let question = questionBox.value;
        socket.send(question);
        thinkingMsg.classList.remove("hidden");
        responseBox.classList.add("hidden");
        answerContainer.classList.remove("hidden");
    };

    let answer = (response) => {
        responseBox.innerText = response;
        thinkingMsg.classList.add("hidden");
        responseBox.classList.remove("hidden");
        questionBox.removeAttribute("disabled");
        askBtn.removeAttribute("disabled");
        questionBox.focus();
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

let questionBox = document.getElementById("question");
var ellipses = document.getElementById("ellipses");

let writeToPlaceholder = (newPlaceholder) => {
    let removal = setInterval(() => {
        let currPlaceholder = questionBox.getAttribute("placeholder");
        if (!currPlaceholder) {
            clearInterval(removal);
            let i = 0;
            let addition = setInterval(() => {
                if (i >= newPlaceholder.length) {
                    clearInterval(addition);
                }
                questionBox.setAttribute("placeholder", newPlaceholder.substring(0, i));
                i++;
            }, 100);
        }
        questionBox.setAttribute("placeholder", currPlaceholder.substring(0, currPlaceholder.length - 1));
    }, 100);
};

setInterval(() => {
    if (ellipses.innerText.length == 2) {
        ellipses.innerText = "";
    } else {
        ellipses.innerText += ".";
    }
}, 150);

let questions = ["Where do I find Hestu in BOTW?", "What is Windblight Ganon's weakness?", "How do I get star fragments in BOTW?"]
let i = 0;
let start = setInterval(() => {
    writeToPlaceholder(questions[i]);
    clearInterval(start);
    i++;
    setInterval(() => {
        writeToPlaceholder(questions[i]);
        i++
        if (i > 2) {
            i = 0;
        }
    }, 8000);
}, 3000);