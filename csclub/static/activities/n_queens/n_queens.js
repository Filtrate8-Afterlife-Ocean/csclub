const completeForm = document.getElementById("completeForm");

const sizeSelect = document.getElementById("sizeSelect");
const newPuzzleBtn = document.getElementById("newPuzzleBtn");
const submitBtn = document.getElementById("submitBtn");

const inputBox = document.getElementById("input");
const answerBox = document.getElementById("answer");
const message = document.getElementById("message");

let n;
let queens;   // queens[row] is the column of the queen in that row, or -1
let fixed;    // fixed[row] is true if the puzzle placed that queen
let solved;

let board = document.getElementById("board");
let square;


function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function isSafe(row) {
    for (let other = 0; other < n; other++) {
        let sameCol = queens[other] === queens[row];
        let sameDiagonal = Math.abs(other - row) === Math.abs(queens[other] - queens[row]);
        if (other !== row && queens[other] !== -1 && (sameCol || sameDiagonal)) {
            return false;
        }
    }
    return true;
}

// Backtracking: put a safe queen in every row, starting each row at a random column
function fillRows(row) {
    if (row === n) {
        return true;
    }

    let start = getRandomInt(n);
    for (let i = 0; i < n; i++) {
        queens[row] = (start + i) % n;
        if (isSafe(row) && fillRows(row + 1)) {
            return true;
        }
    }

    queens[row] = -1;
    return false;
}

function render() {
    board.replaceChildren();
    board.style.setProperty("--n", n);

    for (let row = 0; row < n; row++) {
        for (let col = 0; col < n; col++) {
            square = document.createElement("div");
            square.className = (row + col) % 2 === 0 ? "square" : "square dark";

            if (queens[row] === col) {
                square.textContent = "👑";
                if (solved) {
                    square.classList.add("solved");
                } else if (!isSafe(row)) {
                    square.classList.add("danger");
                } else if (fixed[row]) {
                    square.classList.add("fixed");
                }
            }

            square.onclick = () => placeQueen(row, col);
            board.appendChild(square);
        }
    }
}

function check() {
    let placed = 0;
    let allSafe = true;
    for (let row = 0; row < n; row++) {
        if (queens[row] !== -1) {
            placed++;
            allSafe = allSafe && isSafe(row);
        }
    }

    document.getElementById("queensLeft").textContent = n - placed;
    document.getElementById("worth").textContent = 10 * (n - 3);

    message.textContent = "";
    if (placed === n && allSafe) {
        solved = true;
        message.textContent = "Solved!";
        givePoints();
    } else if (placed === n) {
        message.textContent = "Some queens can attack each other!";
    }

    render();
}

// Each request gives 10 points, so bigger boards send more of them (one at a time)
async function givePoints() {
    for (let i = 0; i < n - 3; i++) {
        await fetch(completeForm.action, { method: "POST", body: new FormData(completeForm) });
    }
}

function placeQueen(row, col) {
    if (solved || fixed[row]) {
        return;
    }
    queens[row] = queens[row] === col ? -1 : col;
    check();
}

function submitAnswer() {
    let lines = answerBox.value.trim().split("\n");
    let answer = [];

    for (let row = 0; row < lines.length; row++) {
        let line = lines[row].replaceAll(" ", "");
        let col = line.indexOf("Q");
        if (line.length === n && col !== -1 && col === line.lastIndexOf("Q") && (!fixed[row] || col === queens[row])) {
            answer.push(col);
        }
    }

    if (solved) {
        return;
    } else if (answer.length !== n || lines.length !== n) {
        message.textContent = "That grid doesn't fit this board.";
    } else {
        queens = answer;
        check();
    }
}

function showInput() {
    let text = "";
    for (let row = 0; row < n; row++) {
        for (let col = 0; col < n; col++) {
            text += queens[row] === col ? "Q" : ".";
        }
        text += "\n";
    }

    inputBox.value = text.trim();
    inputBox.rows = n;
    answerBox.rows = n;
}

function newPuzzle() {
    n = Number(sizeSelect.value);
    queens = new Array(n).fill(-1);
    fillRows(0);

    // Keep a few queens from the solution and clear the rest
    fixed = new Array(n).fill(false);
    let count = 1 + getRandomInt(Math.floor(n / 3));
    while (count > 0) {
        let row = getRandomInt(n);
        if (!fixed[row]) {
            fixed[row] = true;
            count--;
        }
    }
    for (let row = 0; row < n; row++) {
        if (!fixed[row]) {
            queens[row] = -1;
        }
    }

    solved = false;
    answerBox.value = "";
    showInput();
    check();
}

for (let size = 4; size <= 12; size++) {
    sizeSelect.add(new Option(`${size} x ${size}`, size));
}
sizeSelect.value = 6;

newPuzzle();

newPuzzleBtn.onclick = newPuzzle;
sizeSelect.onchange = newPuzzle;
submitBtn.onclick = submitAnswer;
inputBox.onclick = () => inputBox.select();
