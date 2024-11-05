import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go



data = pd.read_csv('data.csv')
data2 = pd.read_csv('data2.csv')
df = pd.DataFrame(data)


with st.sidebar:
    choice = st.selectbox(
        '選擇操作', ['表格','圖表', '比較']
    )
st.title('資料分析_環保葬')
if choice == '表格':
    st.subheader('104~112年環保葬統計')
    df
elif choice == '圖表':
    data = {
        "年別": [104, 105, 106, 107, 108, 109, 110, 111, 112],
        "公園綠地－男": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "公園綠地－女": [0, 0, 0, 0, 0, 0, 0, 0, 0],
        "海洋－男": [13, 19, 19, 19, 15, 12, 14, 20, 25],
        "海洋－女": [2, 6, 3, 8, 15, 10, 9, 4, 9],
        "樹葬－男": [131, 255, 331, 357, 448, 622, 401, 952, 1024],
        "樹葬－女": [47, 76, 134, 170, 223, 272, 778, 514, 532]
    }

    # 創建 DataFrame
    df = pd.DataFrame(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["年別"], y=df["公園綠地－男"], mode='lines+markers', name='公園綠地－男'))
    fig.add_trace(go.Scatter(x=df["年別"], y=df["公園綠地－女"], mode='lines+markers', name='公園綠地－女'))
    fig.add_trace(go.Scatter(x=df["年別"], y=df["海洋－男"], mode='lines+markers', name='海洋－男'))
    fig.add_trace(go.Scatter(x=df["年別"], y=df["海洋－女"], mode='lines+markers', name='海洋－女'))
    fig.add_trace(go.Scatter(x=df["年別"], y=df["樹葬－男"], mode='lines+markers', name='樹葬－男'))
    fig.add_trace(go.Scatter(x=df["年別"], y=df["樹葬－女"], mode='lines+markers', name='樹葬－女'))

    # 顯示圖形
    st.plotly_chart(fig,use_container_width=True)

elif choice == '比較':
    data['總人數－男'] = data[['公園綠地－男', '海洋－男', '樹葬－男']].sum(axis=1)
    data['總人數－女'] = data[['公園綠地－女', '海洋－女', '樹葬－女']].sum(axis=1)

    # 計算第一個檔案的總人數（男+女）
    data['總人數'] = data['總人數－男'] + data['總人數－女']

    # 合併兩個檔案根據年別
    df_merged = pd.merge(data[['年別', '總人數']], data2[['年別', '男性', '女性']], on='年別', how='inner')

    # 計算第二個檔案的總人數（男+女）
    df_merged['總人數_第二個檔案'] = df_merged['男性'] + df_merged['女性']

    # 使用 plotly 繪製長條圖，根據年別比較總人數
    fig = go.Figure(data=[
        go.Bar(name='環保葬人數', x=df_merged['年別'], y=df_merged['總人數']),
        go.Bar(name='全台死亡人數', x=df_merged['年別'], y=df_merged['總人數_第二個檔案'])
    ])

    # 更新圖表的布局
    fig.update_layout(
        barmode='group',  # 並排顯示
        title='每年別的總人數比較',
        xaxis_title='年別',
        yaxis_title='總人數',
        template='plotly'
    )

    st.plotly_chart(fig,use_container_width=True)