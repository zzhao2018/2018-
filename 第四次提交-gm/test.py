from statsmodels.tsa.arima_model import ARMA
import statsmodels.tsa.stattools as st


timeseries = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0]

order = st.arma_order_select_ic(timeseries,max_ar=5,max_ma=5,ic=['aic', 'bic', 'hqic'])




model = ARMA(timeseries, order=order.bic_min_order)
result_arma = model.fit(disp=-1, method='css')

def predict_recover(ts):
    ts = np.exp(ts)
    return ts
train_predict = result_arma.predict()
train_predict = predict_recover(train_predict) #还原
RMSE = np.sqrt(((train_predict-timeseries)**2).sum()/timeseries.size)

predict_ts = result_arma.predict()

for t in range(len(test)):
    model = ARIMA(history, order=(5,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))




