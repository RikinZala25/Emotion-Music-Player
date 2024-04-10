import React, { useState, useMemo, useCallback } from "react";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import MyResponsivePie from "../Charts/pieChart";
import MyResponsiveScatterPlot from "../Charts/scatterplotGraph";

import "./css/audioAcousticsAnalysis.css";

interface Props {
  displayResultData: any;
  selectedSongData: any;
}

interface SongData {
  x: number;
  y: number;
}

const AudioAcousticsAnalysis: React.FC<Props> = ({
  displayResultData,
  selectedSongData,
}) => {
  const audioEmotionPercentages =
    displayResultData.audio_emotion.confidence_scores;
  const audioVA = displayResultData.text_va;

  const selectedSongValence = parseFloat(selectedSongData.valence.toFixed(2));
  const selectedSongArousal = parseFloat(selectedSongData.arousal.toFixed(2));
  const selectedSongDistance = parseFloat(selectedSongData.distance.toFixed(2));

  const [songData, setSongData] = useState<SongData[]>([]);

  const processSongData = useCallback((songs: any[]) => {
    return songs.map((song: any) => ({
      x: parseFloat(song.valence.toFixed(2)),
      y: parseFloat(song.arousal.toFixed(2)),
    }));
  }, []);

  useMemo(() => {
    if (displayResultData) {
      const extractedData = processSongData(displayResultData.suggested_songs);
      const filteredData = extractedData.filter(
        (song) =>
          song.x !== selectedSongValence && song.y !== selectedSongArousal
      );
      setSongData(filteredData);
    }
  }, [
    displayResultData,
    processSongData,
    selectedSongValence,
    selectedSongArousal,
  ]);

  return (
    <>
      <h1>Audio & Acoustics Anaylsis</h1>

      <Grid container spacing={2}>
        <Grid item xs={4}>
          <Box className="speech-emotion-analysis-box">
            <h2>Speech Emotion</h2>
            <p>Speech audio emotion percentages</p>
            <div style={{ height: "250px" }}>
              <MyResponsivePie data={audioEmotionPercentages} />
            </div>
          </Box>

          <h2 className="audio-analysis-h2">Statistics of Selected Song</h2>

          <div
            style={{ marginLeft: "50px" }}
            className="audio-analysis-inner-h2"
          >
            <Grid
              container
              rowSpacing={1}
              columnSpacing={{ xs: 1, sm: 2, md: 3 }}
            >
              <Grid item xs={6}>
                <h2>Valence</h2>
              </Grid>
              <Grid item xs={6}>
                <h2 className="percent-bg">{selectedSongValence}</h2>
              </Grid>
              <Grid item xs={6}>
                <h2>Arousal</h2>
              </Grid>
              <Grid item xs={6}>
                <h2 className="percent-bg">{selectedSongArousal}</h2>
              </Grid>
              <Grid item xs={6}>
                <h2>Distance</h2>
              </Grid>
              <Grid item xs={6}>
                <h2 className="percent-bg">{selectedSongDistance}</h2>
              </Grid>
            </Grid>
          </div>
        </Grid>
        <Grid item xs={8}>
          <Box className="audio-va-space-box">
            <h2>Audio Valence-Arousal (VA) Space</h2>
            <p>
              Coordinates of speech audio and suggested songs on a Valence (x) -
              Arousal (y) plane
            </p>
            <div style={{ height: "500px" }}>
              <MyResponsiveScatterPlot
                data={[
                  {
                    id: "Audio VA",
                    data: [
                      {
                        x: parseFloat(audioVA["valence"].toFixed(2)),
                        y: parseFloat(audioVA["arousal"].toFixed(2)),
                      },
                    ],
                  },
                  {
                    id: "Selected Song VA",
                    data: [
                      {
                        x: selectedSongValence,
                        y: selectedSongArousal,
                      },
                    ],
                  },
                  {
                    id: "Others Songs VA",
                    data: songData,
                  },
                ]}
              />
            </div>
          </Box>
        </Grid>
      </Grid>
    </>
  );
};

export default AudioAcousticsAnalysis;
