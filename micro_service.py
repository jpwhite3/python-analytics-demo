from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as sm

app = Flask(__name__)
api = Api(app)

#  Setup our Prediction model
tips = sns.load_dataset("tips")
tips.rename(columns={'smoker': 'drinker', 'sex': 'gender'}, inplace=True)
formula = 'tip ~ total_bill + size + C(gender) + C(drinker) + C(day) + C(time)'
model = sm.ols(formula, data=tips)    # Describe model
results = model.fit()                 # Fit model 


class PredictTip(Resource):

	def post(self):
		request_data = request.get_json()

		try:
			columns = ['total_bill', 'gender', 'drinker', 'day', 'time', 'size']
			df = pd.DataFrame(request_data, columns=columns)
		except:
			return {'error': 'You posted bad data!'}

		#  Aggrigation & conversion from Numpy types to native types
		bill = df[['total_bill']].sum().item()
		predicted_tip = sum(results.predict(df).tolist())

		return {'bill': bill, 'predicted_tip': round(predicted_tip, 2), 'tip_percentage': round(predicted_tip/bill, 2)}


api.add_resource(PredictTip, '/')

if __name__ == '__main__':
    app.debug = True
    app.run()