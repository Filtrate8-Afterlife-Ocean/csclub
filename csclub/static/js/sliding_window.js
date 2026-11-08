const length = 8;
const fruits = ["🍎", "🍊", "🍐", "🍉"];

const moveLeftBtn  = document.getElementById("moveLeftBtn");
const moveRightBtn  = document.getElementById("moveRightBtn");
const newPuzzleBtn  = document.getElementById("newPuzzleBtn");

let randomFruits;
let left;
let right;
let current;

let seenFruits;
let idx1;
let idx2;
let solution;

let boxes = document.getElementById("boxes");
let slot;
let box;
let pointer;

let fruit;
let duplicate;


function randomItem(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function render() {
    boxes.replaceChildren();

    document.getElementById("solution").textContent = solution;
    document.getElementById("current").textContent = current;

    if (current === solution) {
        document.getElementById("message").textContent = "Solution found!";
    } else if (left >= idx1) {
        document.getElementById("message").textContent = "You skipped it! Try a new puzzle.";
    } else if (duplicate) {
        document.getElementById("message").textContent = "Duplicate fruit added! Try a new puzzle.";
    }

    for (let idx = -1; idx < length; idx++) {
        slot = document.createElement("div");
        slot.className = "slot";
        
        box = document.createElement("div");
        slot.appendChild(box);
        if (idx >= 0) {
            box.className = "box";
            box.textContent = randomFruits[idx];
        } else {
            box.className = "spacer";
        }

        pointer = document.createElement("div");
        pointer.className = "pointer";
        slot.appendChild(pointer);

        if (idx === left || idx === right) {
            if (idx == left) {
                pointer.textContent = "↑\nleft";
            } else {
                pointer.textContent = "↑\nright";
            }
            if (idx >= 0) {
                box.classList.add("selected");
            }
        }

        boxes.appendChild(slot);
    }
}

function moveLeft() {
    if (!duplicate && left < right && left <= idx1) {
        seenFruits.delete(randomFruits[left + 1]);
        left++;
        current--;
        render();
    }
}

function moveRight() {
    if (!duplicate && right < length - 1) {
        if (seenFruits.has(randomFruits[right + 1])) {
            duplicate = true;
        }
        seenFruits.add(randomFruits[right + 1]);
        right++;
        current++;
        render();
    }
}

function getSolution() {
    solution = 0;
    seenFruits = new Set();
    left = 0;
    for (right = 0; right < length; right++) {
        fruit = randomFruits[right];
        while (seenFruits.has(fruit)) {
            seenFruits.delete(randomFruits[left]);
            left++;
        }
        seenFruits.add(fruit);
        let score = right - left + 1;
        if (score > solution) {
            solution = score;
            idx1 = left;
            idx2 = right;
        }
    }
}

function newPuzzle() {
    document.getElementById("message").textContent = "";
    randomFruits = [];
    for (let idx = 0; idx < length; idx++) {
        fruit = randomItem(fruits);
        randomFruits.push(fruit);
    }
    getSolution();
    seenFruits = new Set();
    left = -1;
    right = 0;
    seenFruits.add(randomFruits[0]);
    duplicate = false;
    current = right - left;
    render();
}

newPuzzle();

moveLeftBtn.onclick = moveLeft;
moveRightBtn.onclick = moveRight;
newPuzzleBtn.onclick = newPuzzle;