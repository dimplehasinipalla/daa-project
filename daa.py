from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("front.html")

@app.route("/calculate", methods=["POST"])
def calculate():

    Na = int(request.form["Na"])
    Nb = int(request.form["Nb"])

    x_coords = request.form.getlist("x")
    y_coords = request.form.getlist("y")

    employees = []
    for i in range(len(x_coords)):
        employees.append((i+1,(int(x_coords[i]),int(y_coords[i]))))

    # temporary result
    result = [(1,'B',employees)]

    return render_template("result.html", data=result)

if __name__ == "__main__":
    app.run(debug=True)
