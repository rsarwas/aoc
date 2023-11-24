floors :: [Char] -> [Int]
floors xl = [if x == '(' then 1 else if x == ')' then -1 else 0 | x <- xl] 

finalFloor :: [Char] -> Int
finalFloor = sum . floors 

whenBasement :: [Char] -> Int
whenBasement xl = length $ takeWhile (>=0) $ scanl (+) 0 (floors xl)

main :: IO ()
main = do
    input <- getContents
    putStr "Part 1: "
    print $ finalFloor input
    putStr "Part 2: "
    print $ whenBasement input
