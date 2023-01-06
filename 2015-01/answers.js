function what_floor(text) {
    floor = 0
    for (i = 0; i < len(text); i++) {
        if (text[i] == '(') { floor++ }
        if (text[i] == ')') { floor-- }
    }
    return floor
}

function when_basement(text) {
    floor = 0
    for (i = 0; i < len(text); i++) {
        if (text[i] == '(') { floor++ }
        if (text[i] == ')') { floor-- }
        if (floor == -1) { return i+1 }
    }
    return -1    
}

var stdin = 0;
var fs = require('fs');  // Node only; browser has no filesystem
var input = fs.readFileSync(stdin, 'utf-8');
console.log("Part 1: " + what_floor(input));
console.log("Part 2: " + when_basement(input));
