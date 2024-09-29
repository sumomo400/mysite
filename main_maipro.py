import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import time

# タイトルを表示
st.title('Streamlit test')

st.write('Interactive Widgets')
'Start!!'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iterration{i+1}')
    bar.progress(i+1)
    time.sleep(0.1)

'Done'



left_column, right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write("右カラム")
    
expander = st.expander('問い合わせ')
expander.write('問い合わせ内容を書く')

text = st.text_input('趣味を教えて')
st.write('あなたの趣味：', text)

condition = st.slider('あなたの調子は', 0, 100, 50)
st.write('コンディション：', condition)

# 画像の表示（コメントを外してファイルパスを確認）
img_path = r"C:\Users\ooi31\Desktop\Test.jpg"  # ファイルパスが正しいか確認してください


option = st.selectbox(
    '好きな数字を教えてください。',
    list(range(1,10))
)
'好きな数字は'


try:
    img = Image.open(img_path)
    st.image(img, caption="photo", use_column_width=True)
except FileNotFoundError:
    st.write(f"画像ファイルが見つかりませんでした: {img_path}")



# データフレームのサンプル作成
#data = {
#    'Column A': np.random.randn(10),
#    'Column B': np.random.randn(10),
#    'Column C': np.random.randn(10)
#}
#df = pd.DataFrame(data)

# データフレームをテーブルとして表示
#st.write('データフレーム:')
#st.table(df)

# グラフの描画
#st.line_chart(df)   # 線グラフ
#st.area_chart(df)   # エリアグラフ
#st.bar_chart(df)    # バーチャート

# 地図表示用にランダムな緯度・経度を生成（ストリームリットの地図機能に使う場合）
#map_data = pd.DataFrame(
#    np.random.randn(100, 2) / [50, 50] + [35.69, 139.70],  # 東京周辺の座標を仮定
#    columns=['lat', 'lon']
#)

# 地図を表示
#st.map(map_data)
