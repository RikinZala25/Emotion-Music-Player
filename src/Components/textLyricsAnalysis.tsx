import React from "react";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import MyResponsivePie from "../Charts/pieChart";

import "./css/textLyricsAnalysis.css";

interface Props {
  displayResultData: any;
  selectedSongData: any;
}

const TextLyricsAnalysis: React.FC<Props> = ({
  displayResultData,
  selectedSongData,
}) => {
  const textEmotionPercentages = displayResultData.text_emotion_confidence;
  const lyricsEmotionPercentages = selectedSongData.lyrics_emotion_confidence;

  const detectedText = displayResultData.detected_text;
  const songLyrics = selectedSongData.lyrics.replace(/\n/g, "<br>");

  return (
    <>
      <h1>Text & Lyrics Anaylsis</h1>

      <Grid container rowSpacing={1} columnSpacing={{ xs: 1, sm: 2, md: 3 }}>
        <Grid item xs={6}>
          <Box className="text-emotion-analysis-box">
            <h2>Text Emotion</h2>
            <p>Speech text emotion percentages</p>
            <div style={{ height: "300px" }}>
              <MyResponsivePie data={textEmotionPercentages} />
            </div>
          </Box>
        </Grid>
        <Grid item xs={6}>
          <Box className="lyrics-emotion-analysis-box">
            <h2>Lyrics Emotion</h2>
            <p>Lyrics emotion percentages of selected song</p>
            <div style={{ height: "300px" }}>
              <MyResponsivePie data={lyricsEmotionPercentages} />
            </div>
          </Box>
        </Grid>
        <Grid item xs={6}>
          <Box className="text-emotion-analysis-box">
            <h2>Speech Transcription</h2>
            <p>Transcript recognized from your speech audio</p>
            <div style={{ height: "300px" }}>
              <Box className="text-box">
                <p>{detectedText}</p>
              </Box>
            </div>
          </Box>
        </Grid>
        <Grid item xs={6}>
          <Box className="lyrics-emotion-analysis-box">
            <h2>Lyrics Transcription</h2>
            <p>Lyrics of Selected Song</p>
            <div style={{ height: "300px" }}>
              <Box className="lyrics-box">
                <p dangerouslySetInnerHTML={{ __html: songLyrics }} />
              </Box>
            </div>
          </Box>
        </Grid>
      </Grid>
    </>
  );
};

export default TextLyricsAnalysis;
