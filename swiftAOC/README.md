# swiftAOC

A description of this package.

`$ mkdir Sources/AocLib`
`$ code Package.swift`

replace
```swift
        .target(
            name: "swiftAOC",
            dependencies: []),
```
with
```swift
        .target(
            name: "swiftAOC",
            dependencies: ["AocLib"]),
        .target(name: "AocLib"),
```
and add `AocLib` as a dependency to the `.testTarget`

test with
`swift test`

run with
`swift run swiftAOC 2015-02 < ../2015-02/input.txt`
`swift run -c release swiftAOC 2015-02 < ../2015-02/input.txt`
or
`swift build` or `swift build -c release`
`.build/release/swiftAOC 2015-02 < ../2015-02/input.txt`
`.build/debug/swiftAOC 2015-03 < ../2015-03/input.txt`