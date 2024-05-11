from keras.models import load_model

model = load_model("./model/keras_model.h5")
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
