This is a digital guitar tuner app that helps musicians tune their guitar strings accurately. Here's what makes it special:

1. Core Function:
- Uses your computer's microphone to listen to guitar strings
- Analyzes the sound frequency in real-time
- Compares what it hears to standard guitar tuning frequencies
- Shows how close you are to the correct pitch

2. User-Friendly Interface:
- Six colorful buttons for selecting which string you're tuning (E2, A2, D3, G3, B3, E4)
- Visual meter showing if you're sharp (too high) or flat (too low)
- Color-coded feedback: green for in tune, orange for close, red for off
- Simple start/stop recording controls

3. Technical Details:
- Built with Python using Streamlit for the web interface
- Uses Fast Fourier Transform (FFT) to detect pitch
- Measures in cents (where 100 cents = one semitone)
- Works with standard guitar tuning (E A D G B E)

The app is particularly useful for:
- Beginning guitarists learning to tune by ear
- Quick tuning checks between songs
- Teaching students about proper string pitch
- Visual confirmation of tuning accuracy

To use it, you just need Python installed with a few basic packages (streamlit, numpy, scipy, sounddevice, matplotlib) and a working microphone.
