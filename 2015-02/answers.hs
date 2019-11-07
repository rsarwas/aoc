volume :: Int -> Int -> Int -> Int
volume h w l = h*w*l

surface_area :: Int -> Int -> Int -> Int
surface_area h w l = 2*h*w + 2*h*l + 2*w*l

smallest_side_area :: Int -> Int -> Int -> Int
smallest_side_area h w l = minimum [h*w, h*l, w*l]

smallest_side_perimeter :: Int -> Int -> Int -> Int
smallest_side_perimeter h w l = minimum [2*h+2*w, 2*h+2*l, 2*w+2*l]

paper :: [Int] -> Int
paper (h:w:l:_) = (surface_area h w l) + (smallest_side_area h w l)

ribbon :: [Int] -> Int
ribbon (h:w:l:_) = (volume h w l) + (smallest_side_perimeter h w l)

splitOn     :: Char -> String -> [String]
splitOn c s =  case dropWhile (==c) s of
                      "" -> []
                      s' -> w : splitOn c s''
                            where (w, s'') = break (==c) s'

dims :: String -> [Int]
dims = (map read) . (splitOn 'x')

totalize ::([Int] -> Int) -> String -> Int
totalize f = sum . (map (f . dims)) . lines

main = do
    input <- getContents
    putStr "Part 1: "
    print $ totalize paper input
    putStr "Part 2: "
    print $ totalize ribbon input
