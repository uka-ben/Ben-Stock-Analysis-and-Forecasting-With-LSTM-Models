import numpy as np

from keras.models import Sequential
from keras.layers import Dense , LSTM 
from keras.optimizers import Adam, SGD, RMSprop, Adagrad, Adadelta
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, Normalizer
from sklearn.metrics import mean_absolute_error , mean_squared_error , mean_absolute_percentage_error , r2_score




def scale_data(datasets , scale = 'MinMaxScaler'):

    if scale == "MinMaxScaler" :
        scaler = MinMaxScaler(feature_range=(0,1))
    elif scale == "StandardScaler" : 
        scaler = StandardScaler()
    elif scale == "RobustScaler" : 
        scaler = RobustScaler()
    elif scale == "Normalizer" : 
        scaler = Normalizer()
                  
    scaled_data = scaler.fit_transform(datasets)

    return {"scaled_data" : scaled_data , "scaler": scaler}

def split_num( datasets , size=.8) : 
    train_len = int(np.ceil(len(datasets) * size))
    return train_len


def make_datasets(data) : 
    data= data.filter(['Close'])
    datasets = data.values
    return datasets

def preprocessing(train_len , scaled_data , window=60) : 

    x_train , y_train = train_data (scaled_data=scaled_data , train_len=train_len , window=window) 
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)) 

    return x_train , y_train


def train_data(scaled_data , train_len , window) :

    train_data = scaled_data[0:train_len , :]

    x_train = [] 
    y_train = []

    for i in range(window , len(train_data)):
        x_train.append(scaled_data[i-window : i ,   0])
        y_train.append(scaled_data[i , 0])

    x_train , y_train = np.array(x_train) , np.array(y_train)

    return x_train , y_train


def modelling(x_train , y_train , batch=1 , epoch=1 ,window=60 , learning_rate=0.0001 , optimize='Adam' , loss_function='mean_squared_error' , function_activation='linear'):

    model = Sequential()
    model.add(LSTM(128 , return_sequences=True , input_shape = (window , 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25 ,  activation = function_activation))
    model.add(Dense(1))

    if optimize == "Adam" :
        optimizer = Adam(learning_rate=learning_rate)

    elif optimize == "SGD" : 

        optimizer = SGD(learning_rate = learning_rate)
    elif optimize == "RMSprop" : 

        optimizer = RMSprop(learning_rate = learning_rate)
    elif optimize == "Adagrad" : 

        optimizer = Adagrad(learning_rate = learning_rate)
    elif optimize == "Adadelta" : 

        optimizer = Adadelta(learning_rate = learning_rate)

    model.compile(optimizer=optimizer , loss=loss_function)

    model.fit(x_train, y_train, batch_size=batch, epochs=epoch)

    return model


def test_data (model , scaled_data , train_len , datasets , scaler , window=60) :
        
    test_data = scaled_data[train_len - window: , :]
    # Create the data sets x_test and y_test
    x_test = []
    y_test = datasets[train_len:, :]
    for i in range(window, len(test_data)):
        x_test.append(test_data[i-window:i, 0])

    # Convert the data to a numpy array
    x_test = np.array(x_test)

    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

    # Get the models predicted price values
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    return predictions



def meramal(scaled_data, model, scaler, days , window=60):
    ramalan = []

    # Ambil data 60 hari terakhir
    data = scaled_data[-window:]
    
    for _ in range(days):
        data_temp = data.reshape(1, -1, 1)
        
        # Lakukan prediksi
        predict = model.predict(data_temp)
        
        # Transformasi hasil prediksi ke skala asli
        predict_transformed = scaler.inverse_transform(predict)
        ramalan.append(predict_transformed[0, 0])
        
        # Update data untuk prediksi berikutnya
        # Tambahkan prediksi ke data dan hapus elemen pertama
        data = np.concatenate((data[1:], predict), axis=0)
    
    return np.array(ramalan).reshape(-1)
