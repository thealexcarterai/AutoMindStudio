#!/bin/bash
source .venv/bin/activate

# Step 1: Get trends
python scripts/1_trend_scraper.py

# Step 2: Generate 3 videos
for i in {1..3}; do
    python scripts/2_content_generator.py --auto
    python scripts/3_video_assembler.py
    python scripts/5_copyright_check.py
done

# Step 3: Add watermark to all
find outputs/raw_audio -name "*.wav" | xargs -I {} python scripts/audio_tools.py {} outputs/final_audio/

echo "Automated pipeline completed!"
