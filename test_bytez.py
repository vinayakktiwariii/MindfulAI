from bytez import Bytez

sdk = Bytez("05bb0c56a16725d749100641b2dceaf2")
model = sdk.model("Qwen/Qwen2.5-3B-Instruct")

messages = [
    {"role": "system", "content": "You are a helpful AI"},
    {"role": "user", "content": "Hi, how are you?"}
]

print("Testing Bytez SDK...")
result = model.run(messages)

print(f"\nType: {type(result)}")
print(f"Result: {result}")

if isinstance(result, tuple):
    print(f"Tuple length: {len(result)}")
    for i, item in enumerate(result):
        print(f"Item {i}: {type(item)} = {item}")
