fuel_mass :: Int -> Int
fuel_mass x = x `div` 3 - 2

total_mass :: Int -> Int
total_mass x
    | m <= 0    = 0
    | otherwise = m + total_mass(m)
    where m = fuel_mass(x)

to_ints :: [String] -> [Int]
to_ints = map read

main = do
    input <- getContents
    let modules = to_ints $ lines input
    putStr "Part 1: "
    print $ sum (map fuel_mass modules)
    putStr "Part 2: "
    print $ sum (map total_mass modules)
