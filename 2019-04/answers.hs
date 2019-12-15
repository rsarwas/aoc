cnt v w x y z
  | v == w || w == x || x == y || y == z = 10-z
  | otherwise = 1

cnt' v w x y z
    | v == w && w /= x           = 10-z
    | v /= w && w == x && x /= y = 10-z
    | w /= x && x == y && y /= z = 10-z
    | x /= y && y == z           = 10-z-1
    | y /= z                     = 1
    | otherwise                  = 0

minb x
  | x == 3    = 5
  | otherwise = x

minc x y
  | x == 3 && y == 5 = 9
  | otherwise        = y

t = sum [cnt a b c d e | a <- [3..7], b <- [(minb a)..9], c <- [(minc a b)..9], d <- [c..9], e <- [d..9]]
t' = sum [cnt' a b c d e | a <- [3..7], b <- [(minb a)..9], c <- [(minc a b)..9], d <- [c..9], e <- [d..9]]
