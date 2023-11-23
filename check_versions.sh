# Run all versions of a solution in the current folder
echo
echo "C/C++"
clang --version
echo
echo "C# (mono)"
echo "Disabled until an ARM version is available."
# csc --version
echo
echo "C# (dotnet)"
dotnet --version
echo
echo "dart"
dart --version
echo
echo "Go"
go version
echo
echo "Haskell"
ghc --version
echo
echo "Java"
java --version
echo
echo "Javascript (node)"
node --version
echo
echo "Julia"
julia --version
echo
echo "Python"
python --version
echo
echo "Rust"
rustc --version
echo
echo "Swift"
swiftc --version
echo
echo "Typescript"
tsc --version
