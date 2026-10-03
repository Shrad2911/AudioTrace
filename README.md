\# AudioTrace – Digital Forensic Audio Analyzer



AudioTrace is a web-based digital forensic tool designed to analyze audio files and identify potential indicators of manipulation or unusual signal characteristics.



The tool performs file integrity checks, metadata analysis, waveform analysis, spectrogram analysis, frequency analysis, and basic anomaly detection. It also generates a PDF forensic analysis report.



\## Features



\* Audio file upload

\* MD5 hash generation

\* SHA-256 hash generation

\* File size and format analysis

\* Audio metadata extraction

\* Waveform visualization

\* Spectrogram visualization

\* Frequency spectrum analysis using FFT

\* RMS energy analysis

\* Zero Crossing Rate analysis

\* Silence / low-energy region detection

\* Signal energy variation analysis

\* Sudden signal transition detection

\* PDF forensic report generation



\## Technologies Used



\### Frontend



\* HTML

\* CSS

\* JavaScript



\### Backend



\* Python

\* Flask



\### Audio Analysis



\* Librosa

\* NumPy

\* SciPy

\* FFmpeg / FFprobe



\### Report Generation



\* ReportLab



\## Project Structure



```text

AudioTrace/

│

├── app.py

├── requirements.txt

│

├── modules/

│   ├── hash\_analysis.py

│   ├── metadata.py

│   ├── audio\_analysis.py

│   ├── anomaly\_analysis.py

│   └── report.py

│

├── templates/

│   ├── index.html

│   └── result.html

│

├── static/

│   ├── style.css

│   └── generated analysis images

│

├── uploads/

├── reports/

└── .gitignore

```



\## How It Works



```text

Upload Audio

&#x20;    ↓

File Information

&#x20;    ↓

MD5 \& SHA-256 Hashing

&#x20;    ↓

Metadata Extraction

&#x20;    ↓

Waveform Analysis

&#x20;    ↓

Spectrogram Analysis

&#x20;    ↓

Frequency Analysis

&#x20;    ↓

Signal \& Anomaly Analysis

&#x20;    ↓

Forensic Findings

&#x20;    ↓

PDF Report

```



\## Installation



Clone the repository:



```bash

git clone https://github.com/Shrad2911/AudioTrace.git

```



Open the project folder:



```bash

cd AudioTrace

```



Create a virtual environment:



```bash

python -m venv venv

```



Activate the virtual environment on Windows:



```powershell

venv\\Scripts\\activate

```



Install the required Python libraries:



```bash

pip install -r requirements.txt

```



\## FFmpeg Requirement



AudioTrace uses FFmpeg and FFprobe for audio conversion and metadata extraction.



FFmpeg must be installed separately and its executable paths must be configured in the Python modules.



\## Run the Application



Start the Flask application:



```bash

python app.py

```



Then open:



```text

http://127.0.0.1:5000/

```



Upload an audio file and click \*\*Analyze Audio\*\*.



\## Forensic Disclaimer



AudioTrace reports potential forensic indicators based on file integrity, metadata, and audio signal analysis. The tool does not independently establish that an audio file is authentic, edited, or fake. Further forensic examination and comparison with known-original evidence may be required.



\## Project Purpose



The project was developed as an academic digital forensics project to demonstrate the application of audio signal processing and file analysis techniques in digital forensic investigation.



