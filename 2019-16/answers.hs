base n = (replicate n 0) ++ (replicate n 1) ++ (replicate n 0) ++ (replicate n (-1))
repeater = concat . repeat . base

fft' n input = sum $ zipWith (*) (tail (repeater n)) input
fft'' n input= rem (abs (fft' n input)) 10
fft''' 0 _ = []
fft''' n xs  = (fft'' n xs):(fft''' (n-1) xs)
fft xs = reverse (fft''' (length xs) xs)

phase :: Int -> [Int] -> [Int]
phase 1 xs = fft xs
phase n xs = fft (phase (n-1) xs)

digitToInt c =  fromEnum c - fromEnum '0'

nums s = [digitToInt c | c <- s]

main = do
    input <- getContents
    putStr "Part 1: "
    print $ take 8 (phase 100 (nums input))
