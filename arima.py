from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import joblib


def parser(x):
	return datetime.strptime(x, '%y-%m-%d %H:%M:%S')

series = read_csv('ukdale_def4.csv',header=0,index_col=0,nrows=43640)
print(series['Tv_Dvd_Lamp'].head())


X = series['Gas_Boiler']
size = int(len(X) * 0.86)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()

model = ARIMA(history, order=(5,0,1))
model_fit = model.fit(start_params=[0,0,0,0,0,0,0,1])

maxLen = len(test)

# walk-forward validation
for t in range(len(test)):

	perc = (100 / maxLen) * t
	print(perc)
	print("\nPerc: " + str(perc))

	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)

	model_fit = model_fit.append([test[t]])
	print('predicted=%f, expected=%f' % (yhat, obs))



# evaluate forecasts
rmse = sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)
# plot forecasts against actual outcomes
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()