const length = 8;

const completeForm = document.getElementById("completeForm");

const moveLeftBtn  = document.getElementById("moveLeftBtn");
const moveRightBtn  = document.getElementById("moveRightBtn");
const newPuzzleBtn  = document.getElementById("newPuzzleBtn");

let nums;
let num;
let target;
let left;
let right;

let idx1;
let idx2;
let currentSum;

let boxes = document.getElementById("boxes");
let slot;
let box;
let pointer;


function compareNumbers(a, b) {
    return a - b;
}

function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function render() {
    boxes.replaceChildren();

    document.getElementById("target").textContent = target;
    document.getElementById("sum").textContent = currentSum;

    if (currentSum === target) {
        fetch(completeForm.action, { method: "POST", body: new FormData(completeForm) });
        document.getElementById("message").textContent = "Target found!";
    } else if (left > Math.min(idx1, idx2) || right < Math.max(idx1, idx2)) {
        document.getElementById("message").textContent = "You skipped it! Try a new puzzle.";
    }

    for (let idx = 0; idx < length; idx++) {
        slot = document.createElement("div");
        slot.className = "slot";

        box = document.createElement("div");
        box.className = "box";
        slot.appendChild(box);

        pointer = document.createElement("div");
        pointer.className = "pointer";
        slot.appendChild(pointer);

        if (idx === left || idx === right) {
            if (idx == left) {
                pointer.textContent = "↑\nleft";
            } else {
                pointer.textContent = "↑\nright";
            }
            box.textContent = nums[idx];
            box.classList.add("selected");
        } else {
            box.textContent = "?";
        }

        boxes.appendChild(slot);
    }
}

function moveLeft() {
    if (left < right - 1 && currentSum !== target) {
        left++;
        currentSum = nums[left] + nums[right];
        render();
    }
}

function moveRight() {
    if (right > left + 1 && currentSum !== target) {
        right--;
        currentSum = nums[left] + nums[right];
        render();
    }
}

function newPuzzle() {
    document.getElementById("message").textContent = "";

    nums = [];
    for (let idx = 0; idx < length; idx++) {
        nums.push(getRandomInt(100));
    }
    nums.sort(compareNumbers);
    
    idx1 = getRandomInt(length);
    idx2 = getRandomInt(length);
    while (idx1 === idx2) {
        idx2 = getRandomInt(length);
    }
    target = nums[idx1] + nums[idx2];

    left = 0;
    right = length - 1;
    currentSum = nums[left] + nums[right];

    render();
}

newPuzzle();

moveLeftBtn.onclick = moveLeft;
moveRightBtn.onclick = moveRight;
newPuzzleBtn.onclick = newPuzzle;