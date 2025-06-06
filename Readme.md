
# Tsis.ai 


- [Data Engineering](01_Data_Engineering)


> Optimization in the Real-Time Pattern Detection Process for Active Screens Using ATAS Platform and Scientific Trading Analysis

* [Project Architecture](docs/architecture.md)
* [Repository Structure](docs/structure.md)
* [Technologies Used](docs/technologies.md)
* [Development Status](docs/status.md)
* [How to Contribute](docs/contributing.md)
* [Credits and Purpose](docs/credits.md)

---

This repository contains the main components of the **Tsis.ai** system, a scientific trading assistant that uses real-time screen capture, image recognition, and probabilistic analysis to detect known trading patterns on the ATAS Platform.

The detailed explanations for each module and functionality have been moved to the `docs/` directory to keep this README clean and focused.


---


## Summary

This repository contains the full source code for the **Tsis.ai system**, a scientific assistant for traders based on screen activity analysis, audio reasoning, and probabilistic labeling of trading decisions. The system is designed to work with ATAS and other trading platforms.

## Purpose

The goal is to build a dataset of real trading decisions, enriched with screenshots, videos, transcribed thoughts, and emotional states. This structured data will later be used to train models that detect high-probability trading setups and evaluate the trader's mental state in real time.

## Current Modules

- `manual_region_selector.py` – Selects and saves a region of the screen
- `manual_recording.py` – Allows live screen viewing, starts/stops audio+video recording, saves metadata, and launches labeling
- `label_entry_widgets.py`, `label_entry.py`, `kayzen_scoring.py` – Jupyter-based visual tools for tagging decisions
- `formulari.ipynb` – Interface to review and label captured sessions with Kaizen scores and comments

## Output Structure

Every recording is saved in a session folder:

```
training_data/YYYYMMDD_HHMMSS/
├── region.json
├── metadata.json
├── screenshot.png
├── video.mov
├── audio.wav
├── transcription.txt
├── emotion.json
└── kaizen.json
```

## Workflow Summary

1. Run `manual_region_selector.py` once to select the area of interest
2. Run `manual_recording.py`
3. Press `g` to start recording and `s` to stop (or `q` to quit)
4. The system saves video, audio, metadata, transcribes the audio, and opens the Jupyter notebook for manual labeling

## Goals

- Create a rich labeled dataset of trading decisions
- Train a model that can:
  - Analyze screen content in real time
  - Detect known patterns (visual and verbal)
  - Estimate trader's emotional state (confidence, doubt, anxiety)
  - Suggest probability of trade success before action is taken

## Next Steps

- Finalize Whisper transcription integration and formatting
- Improve `formulari.ipynb` to auto-load session directory
- Build dashboard to browse past sessions
- Prepare model training pipeline
- Build overlay app for real-time probability scoring