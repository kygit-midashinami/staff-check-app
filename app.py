import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---------------------------------------------------------
# 1. 設定部分
# ---------------------------------------------------------
# 【変更】GitHubに上げても安全なように、鍵はクラウドの設定から読み込むように変更
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    # 万が一設定されていない場合のエラー回避
    st.error("APIキーが設定されていません。Streamlit CloudのSecretsを設定してください。")
    st.stop()

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

# プロンプト
CHECK_PROMPT = """
あなたはみずほPayPayドームのサービス向上マネージャーです。
提供されたスタッフの全身画像を分析し、ドームに来場されるお客様をお迎えするのにふさわしいか採点してください。

【チェック基準】
1. 髪型：清潔感、前髪の長さ、髪色の明るさ
2. 制服：シワや汚れ、着こなしのだらしなさ、名札の有無
3. 表情・姿勢：明るい表情（口角）、背筋の伸びた姿勢

【判定基準】
100点満点中で評価し、80点以上ならOK、80点未満ならNG。

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
st.set_page_config(page_title="AI身だしなみチェッカーPro", page_icon="⚾")

st.title("⚾ AI身だしなみチェッカー Pro")

st.info("💡 全身をチェックしますので、カメラから少し離れて、全身が映るように撮影してください。")
st.write("準備ができたら、下の「写真を撮る」ボタンを押してください。")

img_file_buffer = st.camera_input("カメラ起動中...")

if img_file_buffer is not None:
    with st.spinner('チェック中です...'):
        image = Image.open(img_file_buffer)
        try:
            response = model.generate_content([CHECK_PROMPT, image])
            result_text = response.text
            
            st.markdown("---")
            st.subheader("📝 判定結果")
            
            if "判定：OK" in result_text:
                st.success(result_text)
                st.balloons()
            else:
                st.error(result_text)
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")