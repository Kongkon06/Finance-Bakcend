from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.linear_model import LinearRegression

app = FastAPI()

# Train a simple model
expenses = np.array([100, 200, 300, 400, 500]).reshape(-1, 1)
months = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
model = LinearRegression()
model.fit(months, expenses)

# Define request model
class MonthInput(BaseModel):
    month: int

@app.post("/predict")
def predict_expense(data: MonthInput):
    next_month = np.array([[data.month]])
    predicted_expense = model.predict(next_month)[0][0]
    return {"predicted_expense": predicted_expense}

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
