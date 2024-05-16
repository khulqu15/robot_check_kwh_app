import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, InputLayer
from tensorflow.keras.models import Sequential, load_model

def r_squared(y_true, y_pred):
    res = K.sum(K.square(y_true - y_pred))
    tot = K.sum(K.square(y_true - K.mean(y_true)))
    return (1 - res/(tot + K.epsilon()))

data = pd.read_csv('./data/dataset.csv')

data['Tegangan Baterai'] = data['Tegangan Baterai']
data['Arus Beban'] = data['Arus Beban']
data['Arus Beban'] = pd.to_numeric(data['Arus Beban'], errors='coerce')
data['Arus Beban'] = data['Arus Beban'].fillna(data['Arus Beban'].mean())

data.dropna(subset=['SOC'], inplace=True)
data['SOC'] = data['SOC']

print(data)

X = data[['Tegangan Baterai', 'Arus Beban']]
y = data['SOC']

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print(f"X Train: {X_train}")
print(f"y Train: {y_train}")
print(f"X Validation: {X_test}")
print(f"y Validation: {y_test}")

model = Sequential([
    InputLayer(input_shape=(2,)),
    Dense(250, activation='relu'),
    Dense(165, activation='relu'),
    Dense(58, activation='relu'),
    Dense(1, activation='linear'),
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=[r_squared])
history = model.fit(X_train, y_train, epochs=100, validation_split=0.2, batch_size=64)

evaluation = model.evaluate(X_test, y_test)

print(f"Test loss: {evaluation[0]}")
print(f"Test R-squared: {evaluation[1]}")

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("Model has been converted to TensorFlow Lite format.")

def prepare_data(df):
    df['Tegangan Baterai'] = df['Tegangan Baterai'].str.replace(',', '.').astype(float)
    df['Arus Beban'] = df['Arus Beban'].str.replace(',', '.').replace('-', None).astype(float)
    df['Arus Beban'] = pd.to_numeric(df['Arus Beban'], errors='coerce')
    df['Arus Beban'].fillna(df['Arus Beban'].mean(), inplace=True)
    return df

data_with_missing_soc = pd.read_csv('./data/data2.csv')
data_with_missing_soc = prepare_data(data_with_missing_soc)
features = data_with_missing_soc[['Tegangan Baterai', 'Arus Beban']]
scaler = MinMaxScaler()
features_scaled = scaler.fit_transform(features)
predicted_soc = model.predict(features_scaled)

data_with_missing_soc['SOC'] = data_with_missing_soc['SOC'].str.rstrip('%').astype(float) / 100.0 
missing_soc_indices = data_with_missing_soc['SOC'].isna()
data_with_missing_soc.loc[missing_soc_indices, 'SOC'] = predicted_soc[missing_soc_indices]

data_with_missing_soc['SOC'] = (data_with_missing_soc['SOC'] * 100).round(2).astype(str) + '%'
data_with_missing_soc.to_csv('./data/updated_data2.csv', index=False)
print("Updated data with predicted SOC values:")
print(data_with_missing_soc[['Keterangan', 'Menit', 'Tegangan Baterai', 'Arus Beban', 'SOC']])

plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='validation')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()
plt.show()

plt.plot(history.history['r_squared'], label='train R-squared')
plt.plot(history.history['val_r_squared'], label='validation R-squared')
plt.title('Model R-squared')
plt.ylabel('R-squared')
plt.xlabel('Epoch')
plt.legend()
plt.show()