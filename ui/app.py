import streamlit as st
import numpy as np
from PIL import Image
import sys
import os
from streamlit_drawable_canvas import st_canvas

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import HandwritingPredictor
from src.config import MODEL_PATH

st.set_page_config(page_title="HandX")


@st.cache_resource
def load_predictor():
    if os.path.exists(MODEL_PATH):
        return HandwritingPredictor()
    return None

def main():
    st.title("HandX - Digit Recognizer")
    st.subheader("By Mirza Noor Hamza")
    st.write("Draw a digit (0-9) and click Predict")
    
    predictor = load_predictor()
    
    if predictor is None:
        st.error(f"Model not found at {MODEL_PATH}. Please train the model first.")
        st.info("Run: python train_model.py")
        return
    
    if 'canvas_key' not in st.session_state:
        st.session_state.canvas_key = 0
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 255, 1)",
            stroke_width=10,
            stroke_color="#000000",
            background_color="#FFFFFF",
            height=280,
            width=280,
            drawing_mode="freedraw",
            key=f"canvas_{st.session_state.canvas_key}",
            update_streamlit=True
        )
        
        image = None
        if canvas_result.image_data is not None:
            img_array = np.array(canvas_result.image_data)
            if len(img_array.shape) == 3:
                if img_array.shape[2] == 4:
                    img_array = img_array[:, :, :3]
                img_array = np.dot(img_array, [0.2989, 0.5870, 0.1140])
            image = Image.fromarray(img_array.astype(np.uint8))
        
        if image is not None:
            if st.button("Predict"):
                with st.spinner("Processing..."):
                    try:
                        result = predictor.predict(image)
                        st.session_state.prediction_result = result
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("Clear Canvas"):
            st.session_state.canvas_key += 1
            if 'prediction_result' in st.session_state:
                del st.session_state.prediction_result
            st.rerun()
        
        st.write("---")
        result_placeholder = st.empty()
        
        if 'prediction_result' in st.session_state:
            with result_placeholder.container():
                result = st.session_state.prediction_result
                
                st.markdown("### Prediction")
                st.markdown(f"<h1 style='text-align: center; font-size: 48px; margin: 10px 0;'>{result['predicted_digit']}</h1>", unsafe_allow_html=True)
                st.metric("Confidence", f"{result['confidence']*100:.1f}%")
                
                st.write("")
                st.write("**Top 3 guesses:**")
                
                for i, pred in enumerate(result['top_3'], 1):
                    st.write(f"{i}. **{pred['digit']}** - {pred['confidence']*100:.1f}%")

if __name__ == "__main__":
    main()
