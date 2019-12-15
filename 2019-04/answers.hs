cnt v w x y z
  | v == w || w == x || x == y || y == z = 10-z
  | otherwise = 1

minb x
  | x == 3    = 5
  | otherwise = x

minc x y
  | x == 3 && y == 5 = 9
  | otherwise        = y

t = sum [cnt a b c d e | a <- [3..7], b <- [(minb a)..9], c <- [(minc a b)..9], d <- [c..9], e <- [d..9]]
