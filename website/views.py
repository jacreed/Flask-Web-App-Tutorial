from flask import Blueprint, render_template, request, flash, jsonify
import json
import time
import numpy as np
from hdbcli import dbapi
from nelson_siegel_svensson.calibrate import calibrate_ns_ols
from nelson_siegel_svensson import NelsonSiegelCurve
from datetime import datetime
import matplotlib.pyplot as plt

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def BuildCurve():
    print("Im in the python file")
    date = input("Enter the desire date: ")
    type_chosen = input("Choose between swap and govie: ")
    currency = input("Enter the desire currency: ")
    file = type_chosen + "_" + currency + "2"

    conn = dbapi.connect(
        address='localhost',
        port=30015,
        user="S0023847316",
        password="Assassins5creed"
    )

    print('Connected:', conn.isconnected())

    cur = conn.cursor()

    try:
        change_schema = 'SET SCHEMA GROUPE_3_MACHINELEARNING'
        cur.execute(change_schema)
        sql_query = 'SELECT * FROM ? WHERE "Dates"=?'
        cur.execute(sql_query, (file, date))
        records = cur.fetchall()
        t = np.array([])
        y = np.array([])
        for row in records:
            if row[2] and row[1]:
                t = np.append(t, float(row[1]))
                y = np.append(y, float(row[2]))

    except (Exception, dbapi.DatabaseError) as error:
        print(error)
    if conn is not None:
        conn.close()

    curve, status = calibrate_ns_ols(t, y, tau0=1.0)  # starting value of 1.0 for the optimization of tau
    assert status.success
    plt.plot(t, curve(t))
    plt.show()
    
    return jsonify({'_data_': 'gbgbgbg'})
    """
    NS_ZC = NelsonSiegelCurve.zero(curve, t)
    NS_Fwd = NelsonSiegelCurve.forward(curve, t)
    plt.plot(NS_ZC)
    plt.show()
    plt.plot(NS_Fwd)
    plt.show()
    
    """