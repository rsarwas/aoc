import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:math';

void main() async {
  var solution = await solve(packageStream());
  print("Part 1: ${solution.total_paper}");
  print("Part 2: ${solution.total_ribbon}");
}

Future<Solution> solve(Stream<Package> packages) async {
  var solution = Solution();
  await for (final package in packages) {
    solution.add(package);
  }
  return solution;
}

class Solution {
  int total_ribbon = 0;
  int total_paper = 0;

  void add(Package package) {
    total_paper += package.paper;
    total_ribbon += package.ribbon;
  }
}

class Package {
  int w = 0;
  int h = 0;
  int l = 0;

  int get ribbon => volume + smallest_side_perimeter;
  int get paper => surface_area + smallest_side_area;
  int get smallest_side_area => min(h*w, min(h*l, w*l));
  int get smallest_side_perimeter => min(2*h+2*w, min(2*h+2*l, 2*w+2*l));
  int get surface_area => 2*h*w + 2*h*l + 2*w*l;
  int get volume => h*w*l;

  Package(String text) {
  var dims = text.split('x').map((num) {
      return int.tryParse(num) ?? -1;
  });
  this.h = dims.first;
  this.w = dims.elementAt(1);
  this.l = dims.elementAt(2);
  }
}

Stream<Package> packageStream() => 
  stdin.transform(utf8.decoder).transform(const LineSplitter()).transform<Package>(
    StreamTransformer.fromHandlers(handleData: (line, EventSink sink)  => sink.add(Package(line)) )
     );
