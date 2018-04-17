from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import numpy as np
import pandas as pd
import statsmodels.formula.api as sm

app = Flask(__name__)
api = Api(app)

#  Setup our data
tips = pd.read_csv('input/tips.csv')
tips['tip_percent'] = (tips['tip'] / tips['total_bill'] * 100)
tips['tip_above_avg'] = np.where(tips['tip_percent'] >= tips['tip_percent'].mean(), 1, 0)
tips.replace({'Yes': 1, 'No': 0}, inplace=True)

#  Setup our Prediction models
def predict_tip(df):
	formula = 'tip ~ total_bill + party_size + C(ordered_alc_bev) + C(gender) + C(day) + C(time)'
	model = sm.ols(formula, data=tips)    # Describe model
	results = model.fit()                 # Fit model
	return results.predict(df).tolist()

def predict_if_tip_above_avg(df):
	formula = 'tip_above_avg ~ total_bill + party_size + C(ordered_alc_bev) + C(gender) + C(day) + C(time)'
	model = sm.ols(formula, data=tips)    # Describe model
	results = model.fit()                 # Fit model
	return results.predict(df).tolist()


class PredictTip(Resource):

	def post(self):
		request_data = request.get_json()

		try:
			columns = ['total_bill', 'gender', 'ordered_alc_bev', 'day', 'time', 'party_size']
			df = pd.DataFrame(request_data, columns=columns)
		except:
			return {'error': 'You posted bad data!'}

		#  Aggregation & conversion from NumPy types to native types
		total_bill = df[['total_bill']].sum().item()
		predictions = predict_tip(df)
		predicted_tip = sum(predictions)
		predicted_tip_percentage = round(predicted_tip/total_bill, 2)
		predicted_tip_above_average = "Yes" if predicted_tip_percentage >= tips['tip_percent'].mean() else "No"

		return {
            'total_bill': round(total_bill, 2),
			'predicted_tip': round(predicted_tip, 2),
			'tip_percentage': predicted_tip_percentage,
			'tip_above_average': predicted_tip_above_average
		}


api.add_resource(PredictTip, '/')

if __name__ == '__main__':
    app.debug = True
    app.run()
