
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras.saving import register_keras_serializable
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense, Dropout, Reshape
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.losses import MeanSquaredError
import joblib

warnings.filterwarnings('ignore')

# Ensure correct input directory
input_dir = "./kaggle/input"

# Load CSV file
df = pd.read_csv(os.path.join(input_dir, "data.csv"))

# Define columns
variable_expenses = [
    'Groceries', 'Transport', 'Eating_Out', 'Entertainment',
    'Utilities', 'Healthcare', 'Education', 'Miscellaneous'
]
target_columns = [f'Potential_Savings_{cat}' for cat in variable_expenses]
numerical_features = ['Income', 'Age', 'Dependents', 'Disposable_Income', 'Desired_Savings'] + variable_expenses
categorical_features = ['Occupation', 'City_Tier']

# OneHotEncoding categorical features
encoder = OneHotEncoder(drop='first', sparse_output=False)
encoded_cats = encoder.fit_transform(df[categorical_features])
encoded_cat_columns = encoder.get_feature_names_out(categorical_features)
df_encoded_cats = pd.DataFrame(encoded_cats, columns=encoded_cat_columns)

# Combine numerical and categorical features
df_features = pd.concat([df[numerical_features], df_encoded_cats], axis=1)

# Standardization
scaler = StandardScaler()
scaled_numerical = scaler.fit_transform(df_features[numerical_features])
df_scaled_numerical = pd.DataFrame(scaled_numerical, columns=numerical_features, index=df_features.index)
df_features.update(df_scaled_numerical)

# Train-test split
X = df_features
y = df[target_columns]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save encoder & scaler for later use in FastAPI
joblib.dump(encoder, "encoder.pkl")
joblib.dump(scaler, "scaler.pkl")

# Custom Attention Layer
@register_keras_serializable(package="Custom", name="AttentionLayer")
class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(
            name='att_weight', shape=(input_shape[-1], 1),
            initializer='normal', trainable=True
        )
        self.b = self.add_weight(
            name='att_bias', shape=(input_shape[1], 1),
            initializer='zeros', trainable=True
        )
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        e = tf.matmul(x, self.W) + self.b
        e = tf.squeeze(e, -1)
        a = tf.nn.softmax(e)
        a = tf.expand_dims(a, -1)
        output = x * a
        return tf.reduce_sum(output, axis=1)

# Model Architecture
input_dim = X_train.shape[1]
input_layer = Input(shape=(input_dim,))
dense1 = Dense(128, activation='relu')(input_layer)
dropout1 = Dropout(0.3)(dense1)
reshaped = Reshape((128, 1))(dropout1)
attention_output = AttentionLayer()(reshaped)
dense2 = Dense(64, activation='relu')(attention_output)
dropout2 = Dropout(0.3)(dense2)
dense3 = Dense(32, activation='relu')(dropout2)
output_layer = Dense(len(target_columns), activation='linear')(dense3)

model = Model(inputs=input_layer, outputs=output_layer)
model.compile(optimizer='adam', loss=MeanSquaredError(), metrics=['mae'])

# Training
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-5)

history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=64,
    callbacks=[early_stopping, reduce_lr],
    verbose=1
)

model.save("savings_model.h5")
# Save model with AttentionLayer
model = tf.keras.models.load_model(
    "savings_model.h5",
    custom_objects={"AttentionLayer": AttentionLayer}
)



# Evaluation
y_pred = model.predict(X_test)
y_test_df = pd.DataFrame(y_test, columns=target_columns).reset_index(drop=True)
y_pred_df = pd.DataFrame(y_pred, columns=target_columns)

from sklearn.metrics import mean_absolute_error
mae_per_category = {col: mean_absolute_error(y_test_df[col], y_pred_df[col]) for col in target_columns}
for col, mae in mae_per_category.items():
    print(f"MAE for {col}: {mae:.4f}")
