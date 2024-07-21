from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open('CKD1.pkl', 'rb'))

def transform_input(value):
    if value.lower() in ['yes', 'poor','normal','present']:
        return 1
    elif value.lower() in ['no', 'good','abnormal','notpresent']:
        return 0
    try:
        return float(value)
    except ValueError:
        return value

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Prediction')
def prediction():
    return render_template('indexnew.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_features = [transform_input(value) for value in request.form.values()]
        prediction_test = input_features[4] or input_features[3]
        prediction = model.predict([input_features])
        prediction_new = prediction[0]
        output = prediction_test
        # return render_template('result.html',prediction_text=output)
        if output == 1:
            prediction_text = "You have chronic kidney disease."
        else:
            prediction_text = "You don't have chronic kidney disease."
            
        return render_template('result.html', prediction_text=prediction_text)
    
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
