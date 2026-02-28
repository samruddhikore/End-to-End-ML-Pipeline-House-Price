import pickle
import numpy as np

# Load model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

print("Enter feature values separated by comma:")
user_input = input()

values = list(map(float, user_input.split(",")))
values = np.array(values).reshape(1, -1)

prediction = model.predict(values)

print("Predicted House Price:", prediction[0])