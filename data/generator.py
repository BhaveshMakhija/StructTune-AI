import json
import random
import os

def generate_sample():
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"]
    cities = ["New York", "London", "Paris", "Berlin", "Tokyo", "Mumbai"]
    tasks = [
        {"instr": "Extract data: {text}", "schema": {"name": "str", "city": "str"}}
    ]
    
    name = random.choice(names)
    city = random.choice(cities)
    text = f"{name} lives in {city}."
    
    return {
        "instruction": "Extract person name and city into JSON format.",
        "input": text,
        "output": json.dumps({"name": name, "city": city})
    }

def main():
    dataset = [generate_sample() for _ in range(150)]
    os.makedirs("data", exist_ok=True)
    with open("data/dataset.jsonl", "w") as f:
        for entry in dataset:
            f.write(json.dumps(entry) + "\n")
    print(f"✅ Generated 150 samples in data/dataset.jsonl")

if __name__ == "__main__":
    main()
