from pylab import plot, show
from numpy import vstack, array
from numpy.random import rand
from scipy.cluster.vq import kmeans, vq, whiten
import time
from flask import Flask, render_template, request

app = Flask(__name__)
from flask import Flask

from pylab import plot, show
from numpy import vstack, array
from numpy.random import rand
from scipy.cluster.vq import kmeans, vq, whiten
import matplotlib

matplotlib.use('Agg')
import os
import csv



@app.route('/result', methods=['POST', 'GET'])
def test():
    #start_time = time.time()
    if request.method == 'POST':
        mytext = request.form['text1']
        col1 = request.form['text2']
        col2 = request.form['text3']
        K = int(mytext)

        data_arr = []
        meal_name_arr = []

        with open('/home/ubuntu/quiz5/data2.csv', 'rb') as f:
            reader = csv.reader(f)
            for index, row in enumerate(reader):
                if index > 0:
                    #data_arr.append([float(x) for x in row[int(col1):intcol2()]])
                    data_arr.append([float(x) for x in row[9:11]])
                    meal_name_arr.append([row[1]])

        data = vstack(data_arr)
        meal_name = vstack(meal_name_arr)

        # normalization
        data = whiten(data)

        # computing K-Means with K (clusters)
        centroids, distortion = kmeans(data, K)
        print("distortion = " + str(distortion))

        # assign each sample to a cluster
        idx, _ = vq(data, centroids)
        print(meal_name)
        print(data)
        list = []
        for i in range(K):
            result_names = meal_name[idx == i, 0]
            print("=================================")
            print("Cluster " + str(i + 1))
            counter = 0
            for name in result_names:
                counter += 1
            list.append(counter)
            print(counter)
        end_time = time.time()
        total_time = end_time - start_time
        list.append(data)
        list.append(total_time)
        list.append(centroids)
        list = sorted(list,reverse=True)
    return render_template('piechart.html', list=list )


@app.route('/')
def hello_world():
    return render_template('main.html')


port = os.getenv('PORT', '80')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))

