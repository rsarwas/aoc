struct Problem202021: Problem {
  var name: String { "2020-21" }
  func solveWith(data: [String]) -> Solution { Solution202021(data: data) }
}

struct Solution202021: Solution {
  let data: [String]

  var part1: String {
    return "\(answer1)"
  }

  var part2: String {
    return "\(answer2)"
  }

  var answer1: Int {
    let foods = data.compactMap { Food(list: $0) }
    let ingedientMap = foods.ingredientMap
    let allergenMap = foods.allergenMap
    let allergenIngredients = match(allergens: allergenMap, to: foods)
    let allergenIngredient = simplify(allergenIngredients)
    let safeIngredients = remove(allergens: allergenIngredient, from: ingedientMap)
    let count = safeIngredients.values.map { $0.count }.reduce(0, +)
    return count
  }

  var answer2: String {
    let foods = data.compactMap { Food(list: $0) }
    //let ingedientMap = foods.ingredientMap
    let allergenMap = foods.allergenMap
    let allergenIngredients = match(allergens: allergenMap, to: foods)
    let allergenIngredient = simplify(allergenIngredients)
    var ingredients = [String]()
    for allergen in allergenIngredient.keys.sorted() {
      ingredients.append(allergenIngredient[allergen]!)
    }
    return ingredients.joined(separator: ",")
  }

  func match(allergens: [String:[Int]], to foods: [Food]) -> [String:[String]] {
    // match allergen to ingredient
    var ingredients = [String:[String]]()
    for (allergen, foodIndexes) in allergens {
      var ingredientIntersection = Set(foods[foodIndexes.first!].ingredients)
      for index in foodIndexes.dropFirst() {
        ingredientIntersection = ingredientIntersection.intersection(Set(foods[index].ingredients))
      }
      ingredients[allergen] = Array(ingredientIntersection)
    }
    return ingredients
  }

  func simplify(_ map: [String:[String]]) -> [String:String] {
    var allergens = map
    var allergenIngredients = [String: String]()
    var one2oneMatches = allergens.filter { (k,v) in v.count == 1 }
    while one2oneMatches.count > 0 {
      for (k,v) in one2oneMatches {
        let ingredient = v[0]
        // save the one to one matches
        allergenIngredients[k] = ingredient
        //and remove those ingredients from further consideration
        for (k2,v2) in allergens.filter({ _ in true }) { // create a copy for the iteration
          if v2.contains(ingredient) {
            allergens[k2]?.removeAll {$0 == ingredient }
          }
        }
        one2oneMatches = allergens.filter { (k,v) in v.count == 1 }
      }
    }
    return allergenIngredients
  }

  func remove(allergens: [String:String], from: [String:[Int]]) -> [String:[Int]] {
    var ingredients = from
    for badIngredient in allergens.values {
      ingredients.removeValue(forKey: badIngredient)
    }
    return ingredients
  }
}

import Foundation  // for String.components(separatedBy:String)

struct Food {
  let ingredients: [String]
  let allergens: [String]

  init?(list: String) {
    let parts = list.components(separatedBy: " (contains ")
    guard parts.count == 2 else { return nil }
    self.ingredients = parts[0].split(separator: " ").map { String($0) }
    self.allergens = parts[1].dropLast().filter { $0 != " " }.split(separator: ",").map { String($0) }
  }

}

extension Array where Element == Food {
  var ingredientMap: [String:[Int]] {
    var map = [String:[Int]] ()
    for (i,food) in self.enumerated() {
      for item in food.ingredients {
        if !map.keys.contains(item) {
          map[item] = [Int]()
        }
        map[item]?.append(i)
      }
    }
    return map
  }

  var allergenMap: [String:[Int]] {
    var map = [String:[Int]] ()
    for (i,food) in self.enumerated() {
      for item in food.allergens {
        if !map.keys.contains(item) {
          map[item] = [Int]()
        }
        map[item]?.append(i)
      }
    }
    return map
  }

}