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
# 1. Clone or create project
mkdir SHIGL_AI && cd SHIGL_AI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download a local model
# Example: Llama 3.2 3B
mkdir -p ~/.shigl/models
cd ~/.shigl/models
wget https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf

# 5. Set GitHub token (optional)
export GITHUB_TOKEN="your_github_token"

# 6. Run SHIGL AI Center
python -m shigl.cli.main
