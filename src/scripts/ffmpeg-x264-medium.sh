#!/bin/bash
# Video (x264 - 1080p) + Audio (AAC)
# Most quality improving options enabled, medium preset
# Disabled options (rc-lookahead, b-adapt, trellis, me, subme)
# Arguments: 1 (source .mkv file), 2 (destination folder), 3 (tune), 4 (fps), 5 (audio mappings)

ffmpeg -i "$1" -loglevel error -stats -pix_fmt yuv420p -vcodec libx264 -acodec libfdk_aac -map 0:v:0 $5 -map -0:s -map -0:d -map -0:t -vbr 5 -movflags +faststart -preset medium -tune $3 -x264-params "bframes=8:aq-mode=3:aq-strength=0.7:direct=auto:rc-lookahead=72:crf=20:min-keyint=$4" "$2/episode_x264.mp4" 
