var socket = io();
var isThinking = false;

let hide = (elem) => {
    elem.classList.replace("show", "hide");
}
let show = (elem) => {
    elem.classList.replace("hide", "show");
}

// Modified from https://codepen.io/joelewis/pen/ePOrmV
class PlaceholderRotator {
    constructor(options) {
        this.options = options;
        this.element = options.element;
        this.placeholderIdx = 0;
        this.charIdx = 0;
        this.init();
    }

    init = () => {
        this.intervalId = setInterval(this.onTick.bind(this), this.options.speed);
    }

    setPlaceholder = () => {
        let placeholder = this.options.placeholders[this.placeholderIdx];
        var placeholderChunk = placeholder.substring(0, this.charIdx + 1);
        this.element.setAttribute("placeholder", this.options.preText + " " + placeholderChunk);
    };

    onTickReverse = (afterReverse) => {
        if (this.charIdx === 0) {
            afterReverse.bind(this)();
            clearInterval(this.intervalId);
            this.init();
        } else {
            this.setPlaceholder();
            this.charIdx--;
        }
    };

    goReverse = () => {
        clearInterval(this.intervalId);
        this.intervalId = setInterval(this.onTickReverse.bind(this, () => {
            this.charIdx = 0;
            this.placeholderIdx++;
            if (this.placeholderIdx === this.options.placeholders.length) {
                this.placeholderIdx = 0;
            }
        }), this.options.speed);
    };

    onTick = () => {
        var placeholder = this.options.placeholders[this.placeholderIdx];
        if (this.charIdx === placeholder.length) {
            setTimeout(this.goReverse.bind(this), this.options.stay);
        }
        this.setPlaceholder();
        this.charIdx++;
    };

    kill = () => {
        clearInterval(this.intervalId);
    };
}



socket.on("connect", async () => {
    let askBtn = document.getElementById("ask");
    let answerContainer = document.getElementById("answer-container");
    let thinkingMsg = document.getElementById("thinking-message");
    let responseBox = document.getElementById("response");
    let connectingLoaderContainer = document.getElementById("connecting-loader-container");
    let thinkingLoader = document.getElementById("thinking-loader");

    let ask = async () => {
        isThinking = true;
        questionBox.setAttribute("disabled", "");
        askBtn.setAttribute("disabled", "");
        let question = questionBox.value;
        socket.send(question);
        
        responseBox.classList.replace("show", "hide");
        answerContainer.classList.replace("show", "hide");

        await new Promise(r => setTimeout(r, 200));

        thinkingLoader.classList.remove("hidden");
        thinkingMsg.classList.remove("hidden");

        responseBox.innerText = "";
    };

    let answer = (response) => {
        responseBox.innerText = response;

        thinkingMsg.classList.add("hidden");
        thinkingLoader.classList.add("hidden");

        responseBox.classList.replace("hide", "show");

        answerContainer.classList.replace("hide", "show");
        
        questionBox.removeAttribute("disabled");
        askBtn.removeAttribute("disabled");
        questionBox.focus();
        isThinking = false;
    };


    questionBox.addEventListener("input", () => {
        if (questionBox.value) {
            askBtn.removeAttribute("disabled")
        } else {
            askBtn.setAttribute("disabled", "")
        }
    });

    questionBox.addEventListener("keypress", (event) => {
        if (event.key === "Enter" && !isThinking) {
            event.preventDefault();
            ask();
        }
    });

    askBtn.addEventListener("click", ask);
    socket.on("message", answer);
    hide(connectingLoaderContainer)
    show(document.getElementById("page-content"));

    new PlaceholderRotator({
        placeholders,
        stay: 1000,
        speed: 80,
        element: questionBox,
        preText: "How to"
    });

    await new Promise(r => setTimeout(r, 400));
    connectingLoaderContainer.remove();
});

let questionBox = document.getElementById("question");
var ellipses = document.getElementById("ellipses");
let placeholders = [
    "defeat Thunderblight Ganon?", 
    "complete the Etsu Korima Shrine?", 
    "get the Spring-Loaded Hammer?"
]

let dotMap = {
    1: document.getElementById("dot-1"),
    2: document.getElementById("dot-2")
}

var i = 1;
setInterval(() => {
    if (i > 2) {
        i = 1;
        dotMap[1].classList.add("invisible");
        dotMap[2].classList.add("invisible");
    } else {
        console.log(i)
        console.log(dotMap[i])
        let currDot = dotMap[i];
        currDot.classList.remove("invisible");
        i++; 
    }
}, 150);