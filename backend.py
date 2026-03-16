from flask import Flask, render_template, request
import math

app = Flask(__name__)

def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def nearest_neighbor(start, employees):

    remaining = employees[:]
    route=[]
    current=start

    while remaining:
        nearest=min(remaining,key=lambda x:manhattan(current,x[1]))
        route.append(nearest)
        current=nearest[1]
        remaining.remove(nearest)

    return route


def assign_cabs(Na,Nb,employee_coords):

    depot=(0,0)

    employees=[(i+1,coord) for i,coord in enumerate(employee_coords)]

    employees_with_angle=[]

    for emp in employees:
        x,y=emp[1]
        angle=math.atan2(y,x)
        employees_with_angle.append((emp[0],emp[1],angle))

    employees_with_angle.sort(key=lambda x:x[2])

    sorted_emp=[(e[0],e[1]) for e in employees_with_angle]

    cabs=[]
    index=0
    cab_id=1

    for _ in range(Nb):

        group=sorted_emp[index:index+8]

        if not group:
            break

        route=nearest_neighbor(depot,group)

        cabs.append((cab_id,"B",route))

        cab_id+=1
        index+=8

    for _ in range(Na):

        group=sorted_emp[index:index+4]

        if not group:
            break

        route=nearest_neighbor(depot,group)

        cabs.append((cab_id,"A",route))

        cab_id+=1
        index+=4

    return cabs


@app.route("/")
def home():
    return render_template("front.html")


@app.route("/calculate",methods=["POST"])
def calculate():

    Na=int(request.form["Na"])
    Nb=int(request.form["Nb"])

    xs=request.form.getlist("x")
    ys=request.form.getlist("y")

    employees=[]

    for i in range(len(xs)):
        employees.append((int(xs[i]),int(ys[i])))

    cabs=assign_cabs(Na,Nb,employees)

    return render_template("result.html", cabs=cabs)

if __name__ == "__main__":
    app.run(debug=True)
