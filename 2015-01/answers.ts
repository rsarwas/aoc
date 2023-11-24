function what_floor(text: string): number {
    var floor = 0
    for (const c of text) {
        if (c == '(') { floor++; }
        if (c == ')') { floor--; }
    }
    return floor
}

function when_basement(text: string): number {
    var floor = 0;
    var move_number = 0;
    for (const char of text) {
        move_number++;
        if (char == '(') { floor++; }
        if (char == ')') { floor--; }
        if (floor == -1) { return move_number; }
    }
    return -1;
}

const stdin = 0;
const fs = require('fs');  // Node only; browser has no filesystem
const input: string = fs.readFileSync(stdin, 'utf-8');
console.log("Part 1: " + what_floor(input));
console.log("Part 2: " + when_basement(input));
