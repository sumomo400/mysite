import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st
from datetime import datetime, timedelta

st.title('株価チャート')

st.sidebar.write("""
# 株価 
チャートを閲覧できます。                        
""")

st.sidebar.write("""
## 表示日数選択
""")

# 日数のスライダー
days = st.sidebar.slider('日数', 1, 50, 20)

# f-string を使って日数を正しく表示
st.write(f"""
### 過去 **{days}日間** の株価         
""")

@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(start=start_date, end=end_date)
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    ### 株価の範囲指定
    """)

    # スライダーで範囲指定
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください',
        0.0, 3500.0, (0.0, 3500.0)
    )

    tickers = {
        'SPY': 'SPY',
        'QQQ': 'QQQ',
        'VYM': 'VYM',
    }

    # データ取得
    df = get_data(days, tickers)

    # ティッカー選択（`multiselect`に修正）
    companies = st.multiselect(
        'ティッカーを選択してください',
        list(df.index),
        ['SPY', 'QQQ', 'VYM']
    )

    if not companies:
        st.error('少なくとも１つ選択してください。')
    else:
        data = df.loc[companies]
        st.write("### 株価（USD）", data.sort_index())

        # データを変換
        data = data.T.reset_index().rename(columns={'index': 'Date'})
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices (USD)'}
        )

        # Altairのチャート作成、範囲指定のscaleを追加
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices (USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )

        # チャートを表示
        st.altair_chart(chart, use_container_width=True)
except:
    st.error("""エラーが発生しています""")
    