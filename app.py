from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import folium

app = Flask(__name__)
df = pd.read_excel('assignment/도로교통공단_전국_사망교통사고정보(2018).xlsx')


@app.route('/')
def hello_world():
    return render_template('base.html')


@app.route("/mapview")
def mapViewFn():
    map = folium.Map(location=[37.602829, 127.039508], zoom_start=12)

    for i in range(len(df)):
        if df['발생지시군구'][i] == '성북구':
            mk = folium.Marker([df['위도'][i], df['경도'][i]], popup='<p>' + df['법규위반'][i] + '</p>')
            mk.add_to(map)

    map.save('templates/map.html')

    return render_template('mapview.html')


@app.route("/map")
def mapFn():
    return render_template('map.html')


@app.route("/day")
def dayFn():
    seoul = df.groupby(['발생지시도', '요일'])
    a = seoul.sum().loc['서울'][['사망자수', '사상자수']]
    return render_template('day.html', data=a)
    # return a.to_html()


@app.route("/death/busan")
def d_busan():
    # a = df[df['발생지시도'] == '부산'][['사망자수']]
    d_busan_sum = df[df['발생지시도'] == '부산']['사망자수'].sum()
    # return render_template('d_busan.html', data1=a, data=d_busan_sum)
    return render_template('d_busan.html', data=d_busan_sum)


@app.route("/seoul/mon")
def seoul_mon():
    seoul_mon = df[(df['발생지시도'] == '서울') & (df['요일'] == '월')][['발생지시도', '사상자수', '사고유형', '법규위반']]
    return render_template('seoul_mon.html', data=seoul_mon)


@app.route("/cross")
def cross():
    cross_r = df[df['사고유형'] == '횡단중'][['요일', '법규위반', '피해자_당사자종별']]
    return render_template('cross.html', data=cross_r)


if __name__ == '__main__':
    app.run(debug=True)
