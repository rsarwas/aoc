import 'dart:async';
import 'dart:convert';
import 'dart:io';

void main() {
  readLine().listen(processLine);
}

Stream<String> readLine() =>
    stdin.transform(utf8.decoder).transform(const LineSplitter());

void processLine(String line) {
  print("Part 1: ${whatFloor(line)}");
  print("Part 2: ${whenBasement(line)}");
}

final up = "(".codeUnitAt(0);
final down = ")".codeUnitAt(0);

int whatFloor(String input) {
  var floor = 0;
  input.runes.forEach((int rune) {
    if (rune == up) floor += 1;
    if (rune == down) floor -= 1;
  });
  return floor;
}

int whenBasement(String input) {
  var floor = 0;
  //you cannot break out of a dart .forEach early
  for (int i = 0; i < input.length; i++) {
    var rune = input.codeUnitAt(i);
    if (rune == up) floor += 1;
    if (rune == down) floor -= 1;
    if (floor == -1) return i + 1;
  }
  return -1;
}
