// swift-tools-version:5.9
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
  name: "swiftAOC",
  platforms: [
    //.macOS(.v10_15) // Required for CryptoKit in 2015-04
    .macOS(.v13)  // Required for String.split() in 2015-06
  ],
  dependencies: [
    // Dependencies declare other packages that this package depends on.
    // .package(url: /* package url */, from: "1.0.0"),
  ],
  targets: [
    // Targets are the basic building blocks of a package. A target can define a module or a test suite.
    // Targets can depend on other targets in this package, and on products in packages this package depends on.
    .executableTarget(
      name: "swiftAOC",
      dependencies: ["AocLib"]),
    .target(name: "AocLib"),
    .testTarget(
      name: "swiftAOCTests",
      dependencies: ["AocLib"]),
  ]
)
