import streamlit as st, pandas as pd, numpy as np
from myControls import list_cases,list_cases_simple,select_case_by_index, AI_answer

if 'df' not in st.session_state:
    st.session_state.df=pd.DataFrame(
        list_cases_simple(0,171),columns=['No','Sex','Age','Main problem','Dep','ASD','ADHD'],
    )
st.set_page_config(layout="wide")
st.title('人工智能兒青精神病史區辨系統 (試用版)')
st.divider()
##st.write(f"雲端AI模型區辨結果(%):{AI_answer(myHx)}")
@st.dialog('AskAI dialog')
def show_dialog():
    myHx=st.text_area('輸入病史後請按ctrl+enter鍵')
    if st.button('送出'):
        st.session_state.myHx=myHx
        st.rerun()
if st.button('輸入病史Ask AI'):
    show_dialog()
if 'myHx' in st.session_state:
    st.write(f"輸入病史:{st.session_state.myHx}")
    st.divider()
    st.write(f"雲端AI模型區辨結果(%):{AI_answer(st.session_state.myHx)}")
st.divider()
st.header('參考兒青住院病歷:')
event=st.dataframe(
    st.session_state.df,
    key='data',
    on_select='rerun',
    selection_mode='single-row',
    hide_index=True,
    height=400,
)
st.divider()
st.header('所選擇之參考病歷:')
if event and event.selection:
    try: 
        caseID=str(event.selection['rows'][0])
        st.write(f"no:{caseID}")
        myCase=select_case_by_index(caseID)
        st.write(f"現在病史:{myCase['現在病史']}")
        st.divider()
        st.header('雲端LLM與地端LLM預處理結果:')
        st.write(f"""病歷診斷(出院時病歷登錄診斷):
                    憂鬱症: {myCase['DEP']} , 
                    自閉症:{myCase['ASD']} , 
                    注意力不足過動症:{myCase['ADHD']}
                    """)
        st.write(f"""雲端LLM診斷(微軟 gpt-4o):
                    憂鬱症: {myCase['pDEPgpt']}% , 
                    自閉症:{myCase['pASDgpt']}% , 
                    注意力不足過動症:{myCase['pADHDgpt']}%
                    """)
        st.write(f"""地端LLM診斷(未使用RAG技術):
                    憂鬱症: {myCase['pDEPm']}% , 
                    自閉症:{myCase['pASDm']}% , 
                    注意力不足過動症:{myCase['pADHDm']}%
                    """)
        st.write(f"""地端LLM診斷(使用RAG技術):
                    憂鬱症: {myCase['pDEPrag']}% , 
                    自閉症:{myCase['pASDrag']}% , 
                    注意力不足過動症:{myCase['pADHDrag']}%
                    """)
    except Exception as e:
        st.write("請點選上方資料表最左空格,選取查詢個案....😊")