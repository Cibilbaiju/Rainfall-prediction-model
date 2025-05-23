import os

# Check where Python is currently working from
print("Working directory:", os.getcwd())

# Create a simple accuracy value
accuracy = 88.77

# Build the file path to model_accuracy.txt in the same folder
accuracy_path = os.path.join(os.path.dirname(__file__), 'model_accuracy.txt')

# Show where it's about to save
print("Writing to:", accuracy_path)

# Write the value into model_accuracy.txt
with open(accuracy_path, 'w') as f:
    f.write(str(accuracy))

print("✅ Test write successful.")
