// SHIGL 2.0 - A modern systems language

// Variables
let name: string = "Erfan"
let age: int = 25
let scores: list<int> = [90, 85, 88]

// Functions
fn greet(name: string) -> string {
    return "Hello, " + name
}

// Conditional
if age >= 18 {
    print("Adult")
} else {
    print("Minor")
}

// Loops
for i in 0..10 {
    print(i)
}

// Android module
android app "MyApp" {
    minSdk = 21
    targetSdk = 34
    
    activity "MainActivity" {
        layout = "main"
        text = "Hello SHIGL!"
    }
}