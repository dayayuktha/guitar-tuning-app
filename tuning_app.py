import streamlit as st
import numpy as np
import sounddevice as sd
from scipy.fftpack import fft
import time
import matplotlib.pyplot as plt

# Set page configuration with a dark theme
st.set_page_config(
    page_title="Guitar Tuner",
    page_icon="🎸",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        margin: 5px;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .big-text {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def detect_pitch(audio_data, sample_rate):
    """
    Detect the fundamental frequency (pitch) from audio data using FFT
    """
    window = np.hanning(len(audio_data))
    audio_data = audio_data * window
    
    fft_data = fft(audio_data)
    freqs = np.fft.fftfreq(len(fft_data), 1.0/sample_rate)
    
    magnitude = np.abs(fft_data)
    peak_freq = freqs[np.argmax(magnitude)]
    
    return abs(peak_freq)

def get_note_match(frequency, target_note):
    """
    Compare detected frequency with target note
    """
    NOTES = {
        'E2': 82.41,
        'A2': 110.00,
        'D3': 146.83,
        'G3': 196.00,
        'B3': 246.94,
        'E4': 329.63
    }
    
    target_freq = NOTES[target_note]
    cents_off = 1200 * np.log2(frequency / target_freq)
    
    return target_freq, cents_off

def create_tuning_meter(cents):
    """
    Create a visual tuning meter using matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 2))
    
    # Define the range and colors
    x_range = np.linspace(-50, 50, 100)
    colors = ['#ff6b6b', '#ffd93d', '#6bff6b', '#ffd93d', '#ff6b6b']
    
    # Create gradient background
    for i in range(4):
        ax.axvspan(-50 + 25*i, -25 + 25*i, color=colors[i], alpha=0.3)
        ax.axvspan(-25 + 25*i, 0 + 25*i, color=colors[i+1], alpha=0.3)
    
    # Add indicator needle
    cents = max(min(cents, 50), -50)  # Clamp value
    ax.plot([cents, cents], [-1, 1], color='black', linewidth=3)
    
    # Customize appearance
    ax.set_xlim(-50, 50)
    ax.set_ylim(-1, 1)
    ax.set_xticks([-50, -25, 0, 25, 50])
    ax.set_xticklabels(['Too Low', '', 'In Tune', '', 'Too High'])
    ax.set_yticks([])
    ax.grid(True, alpha=0.3)
    
    return fig

def main():
    st.title("🎸 Interactive Guitar Tuner")
    st.write("Select your target note and use your microphone to tune!")
    
    # Audio parameters
    SAMPLE_RATE = 44100
    DURATION = 2
    
    # Initialize session state
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    
    # Note selection buttons in two rows
    st.markdown("### Select Target Note")
    col1, col2, col3 = st.columns(3)
    with col1:
        e2_button = st.button("Low E (E2)", key="E2")
    with col2:
        a2_button = st.button("A (A2)", key="A2")
    with col3:
        d3_button = st.button("D (D3)", key="D3")
        
    col4, col5, col6 = st.columns(3)
    with col4:
        g3_button = st.button("G (G3)", key="G3")
    with col5:
        b3_button = st.button("B (B3)", key="B3")
    with col6:
        e4_button = st.button("High E (E4)", key="E4")
    
    # Update selected note based on button clicks
    if 'selected_note' not in st.session_state:
        st.session_state.selected_note = 'E2'
    
    for note in ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']:
        if st.session_state.get(note):
            st.session_state.selected_note = note
    
    st.markdown(f"### Currently tuning: **{st.session_state.selected_note}**")
    
    # Recording control buttons
    col_rec1, col_rec2 = st.columns(2)
    with col_rec1:
        if st.button("🎤 Start Recording", key="start"):
            st.session_state.is_recording = True
    with col_rec2:
        if st.button("⏹️ Stop Recording", key="stop"):
            st.session_state.is_recording = False
    
    # Display areas
    status = st.empty()
    meter = st.empty()
    result = st.empty()
    
    while st.session_state.is_recording:
        status.markdown("### 🎧 Listening...")
        
        # Record audio
        audio_data = sd.rec(int(DURATION * SAMPLE_RATE),
                          samplerate=SAMPLE_RATE,
                          channels=1)
        sd.wait()
        
        # Process audio
        frequency = detect_pitch(audio_data.flatten(), SAMPLE_RATE)
        expected_freq, cents = get_note_match(frequency, st.session_state.selected_note)
        
        # Create and display tuning meter
        fig = create_tuning_meter(cents)
        meter.pyplot(fig)
        plt.close(fig)
        
        # Display results with colored text
        if abs(cents) <= 5:
            status_color = "#4CAF50"  # Green
            status_text = "Perfect! 🎯"
        elif abs(cents) <= 15:
            status_color = "#FFA500"  # Orange
            status_text = "Close! 👍"
        else:
            status_color = "#FF4444"  # Red
            status_text = "Keep adjusting! 🔄"
        
        result.markdown(f"""
        <div style='background-color: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>
            <p style='color: {status_color}; font-size: 24px; font-weight: bold;'>{status_text}</p>
            <p>Detected Frequency: {frequency:.1f} Hz</p>
            <p>Expected Frequency: {expected_freq:.1f} Hz</p>
            <p>Cents Off: {cents:.1f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.1)
    
    status.write("Ready to tune! Press 'Start Recording' to begin.")

if __name__ == "__main__":
    main()