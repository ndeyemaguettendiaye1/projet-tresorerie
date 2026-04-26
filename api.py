from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/previsions')
def previsions():
    df = pd.read_excel("previsions_tresorerie_resultats.xlsx")
    df = df[['ds', 'yhat', 'optimiste', 'pessimiste']]
    return jsonify(df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=False)