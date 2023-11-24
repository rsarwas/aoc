volume :: Int -> Int -> Int -> Int
volume h w l = h * w * l

surfaceArea :: Int -> Int -> Int -> Int
surfaceArea h w l = 2 * h * w + 2 * h * l + 2 * w * l

smallestSideArea :: Int -> Int -> Int -> Int
smallestSideArea h w l = minimum [h * w, h * l, w * l]

smallestSidePerimeter :: Int -> Int -> Int -> Int
smallestSidePerimeter h w l = minimum [2 * h + 2 * w, 2 * h + 2 * l, 2 * w + 2 * l]

paper :: [Int] -> Int
paper (h : w : l : _) = surfaceArea h w l + smallestSideArea h w l

ribbon :: [Int] -> Int
ribbon (h : w : l : _) = volume h w l + smallestSidePerimeter h w l

splitOn :: Char -> String -> [String]
splitOn c s = case dropWhile (== c) s of
  "" -> []
  s' -> w : splitOn c s''
    where
      (w, s'') = break (== c) s'

dims :: String -> [Int]
dims = map read . splitOn 'x'

totalize :: ([Int] -> Int) -> String -> Int
totalize f = sum . map (f . dims) . lines

main :: IO ()
main = do
  input <- getContents
  putStr "Part 1: "
  print $ totalize paper input
  putStr "Part 2: "
  print $ totalize ribbon input
