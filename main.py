from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    name = "Engineers"
    return render_template('index.html', title='flask test', name=name)

@app.route('/test')
def good():
    name = "test"
    return name

if __name__ == "__main__":
    app.run(debug=True)
