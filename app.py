import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---------------------------------------------------------
# 1. 設定部分
# ---------------------------------------------------------
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("APIキーが設定されていません。Streamlit CloudのSecretsを設定してください。")
    st.stop()

genai.configure(api_key=API_KEY)

# 推奨モデル
model = genai.GenerativeModel('gemini-2.5-flash')

# プロンプト（エンタメ複合施設・上半身・名札必須）
CHECK_PROMPT = """
あなたはエンタメ複合施設のサービス向上マネージャーです。
提供されたスタッフの「上半身の画像」を分析し、施設に来場されるお客様をお迎えするのにふさわしいか採点してください。

【チェック基準】
1. 髪型：
・清潔感があるか
・前髪が長く目にかかっていないか（長い場合は結んでいるか）
・髪色が明るすぎないか

2. 制服・名札（重要）：
・【必須】ひらがな名札はハッキリと装着されているか
・シャツや服に目立つシワや汚れがないか
・襟元などがだらしなくないか

3. 表情：
・口角が上がっており、明るく話しかけやすい表情か

【判定基準】
100点満点中で評価し、80点以上ならOK、80点未満ならNG。
特に「名札が見えない」場合は厳しく減点してください。

【出力形式】
以下の見出しフォーマットを厳守して出力してください。

# 判定：OK（○点）
※NGの場合は「# 判定：NG（○点）」

## 良い点👍
* （良かった点を箇条書き）

## 改善点😿
* （改善すべき点を箇条書き）
"""

# ---------------------------------------------------------
# 2. アプリの画面構成（GUI）
# ---------------------------------------------------------
st.set_page_config(page_title="AI身だしなみチェッカーPro", page_icon="✨")

st.title("✨ AI身だしなみチェッカー Pro")

# 案内文
st.info("💡 上半身（胸から上）をチェックします。「名札」がハッキリ写るように撮影してください。")

# 【追加】カメラ切り替えに関する案内（アコーディオン形式）
with st.expander("📷 外カメラ/内カメラの切り替え方法"):
    st.write("スマホでご利用の場合、下のカメラ画面の中に**「カメラの切り替えアイコン」**または**「カメラを選択」**というメニューが表示されます。そちらをタップして切り替えてください。")

st.write("準備ができたら、下の「写真を撮る」ボタンを押してください。")

# カメラ入力ウィジェット
img_file_buffer = st.camera_input("カメラ起動中...")

if img_file_buffer is not None:
    with st.spinner('チェック中です...'):
        
        # 1. 画像変換
        image = Image.open(img_file_buffer)

        # 2. Geminiに送信して判定
        try:
            response = model.generate_content([CHECK_PROMPT, image])
            result_text = response.text
            
            # 3. 結果の表示
            st.markdown("---")
            st.subheader("📝 判定結果")
            
            if "判定：OK" in result_text:
                st.success(result_text)
                st.balloons()
            else:
                st.error(result_text)
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")