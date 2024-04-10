import React from "react";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";

import OutputBoxRenderer from "./outputBoxRenderer";
import MyResponsiveRadar from "../Charts/radarChart";

import "./css/overallAnalysis.css";

interface Props {
  selectedSongData: any;
  displayDetectedEmotion: string;
}

const OverallAnalysis: React.FC<Props> = ({
  selectedSongData,
  displayDetectedEmotion,
}) => {
  
  const overallSimilarity = selectedSongData.overall_similarity.toFixed(2);
  const acousticSimilarity = selectedSongData.acoustic_similarity.toFixed(2);
  const textSimilarity = selectedSongData.text_similary.toFixed(2);
  const semanticsSimilarity = selectedSongData.semantics_similarity.toFixed(2);

  let artistsString = selectedSongData.artists.join(", ");

  let songString = selectedSongData.name;

  let maxCharacters = 80;

  if (artistsString.length > maxCharacters) {
    artistsString = artistsString.substring(0, maxCharacters - 3) + "...";
  }

  if (songString.length > maxCharacters) {
    songString = songString.substring(0, maxCharacters - 3) + "...";
  }

  const handleClick = () => {
    console.log("Button Clicked");
  };

  return (
    <>
      <h1>Overall Anaylsis</h1>

      <Grid container spacing={2}>
        <Grid item xs={8} style={{ textAlign: "left", marginLeft: "30px" }}>
          <h1 className="overall-analysis-h1">Song Name: {songString}</h1>
          <h2 className="overall-analysis-h2">Artists: {artistsString}</h2>

          <div className="more-info-box-inner-div">
            <OutputBoxRenderer
              showMusicPercentDiv={false}
              displayData={selectedSongData}
              handleClick={handleClick}
            />
          </div>

          <div className="overall-analysis-details-h2">
            <Grid
              container
              rowSpacing={1}
              columnSpacing={{ xs: 1, sm: 2, md: 3 }}
            >
              <Grid item xs={6}>
                <h2>Your Emotion:</h2>
              </Grid>
              <Grid item xs={6}>
                <h2 className="genenerated-emotion-label">
                  {displayDetectedEmotion}
                </h2>
              </Grid>
              <Grid item xs={6}>
                <h2>
                  Overall Similarity: &emsp;
                  <span className="percent-bg">{overallSimilarity} %</span>
                </h2>
              </Grid>
              <Grid item xs={6}>
                <h2>
                  Acousic Similarity: &emsp;
                  <span className="percent-bg">{acousticSimilarity} %</span>
                </h2>
              </Grid>
              <Grid item xs={6}>
                <h2>
                  Text Similarity: &emsp;
                  <span className="percent-bg">{textSimilarity} %</span>
                </h2>
              </Grid>
              <Grid item xs={6}>
                <h2>
                  Semantics Similarity: &emsp;
                  <span className="percent-bg">{semanticsSimilarity} %</span>
                </h2>
              </Grid>
            </Grid>
          </div>
        </Grid>
        <Grid item xs={4} style={{ marginLeft: "-60px" }}>
          <Box className="overall-analysis-box">
            <h2>Speech and Song Similarity</h2>
            <div style={{ height: "250px" }}>
              <MyResponsiveRadar
                data={[
                  {
                    label: "Text",
                    value: parseFloat(textSimilarity),
                  },
                  {
                    label: "Acoustic",
                    value: parseFloat(acousticSimilarity),
                  },
                  {
                    label: "Semantics",
                    value: parseFloat(semanticsSimilarity),
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

export default OverallAnalysis;
