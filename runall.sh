# Run all versions of a solution in the current folder
echo
echo "C/C++"
clang answers.c && ./a.out < input.txt && rm a.out
echo
echo "C# (mono)"
echo "Disabled until an ARM version is available."
# csc answers.cs && mono answers.exe < input.txt && rm answers.exe
echo
echo "C# (dotnet)"
../run_dotnet.sh answers input.txt
echo
echo "dart"
dart run answers.dart < input.txt
echo
echo "Go"
go run answers.go < input.txt
echo
echo "Haskell"
ghc -v0 answers.hs && ./answers < input.txt && rm answers answers.hi answers.o
echo
echo "Java"
java answers.java < input.txt
echo
echo "Javascript (node)"
node answers.js < input.txt
echo
echo "Julia"
julia answers.jl < input.txt
echo
echo "Python"
python answers.py < input.txt
echo
echo "Rust"
rustc answers.rs && ./answers < input.txt && rm answers
echo
echo "Swift"
swiftc answers.swift && ./answers < input.txt && rm answers
echo
echo "Typescript"
# target above es5 generates `error TS2792: Cannot find module 'undici-types'`
# tsc answers.ts --outFile answers.ts.js --target es2018 && node answers.ts.js < input.txt && rm answers.ts.js
tsc answers.ts --strict --outFile answers.ts.js && node answers.ts.js < input.txt && rm answers.ts.js
