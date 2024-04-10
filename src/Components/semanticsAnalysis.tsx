import React from "react";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import MyResponsiveHeatMap from "../Charts/heatmapGraph";

import "./css/semanticsAnalysis.css";

interface Props {
  displayResultData: any;
  selectedSongData: any;
}

const SemanticsAnalysis: React.FC<Props> = ({
  displayResultData,
  selectedSongData,
}) => {
  
  const speechKeywords = displayResultData.input_text_keywords;

  const lyricsKeywords = selectedSongData.lyrics_keywords;

  const keywordsSimilarity = selectedSongData.keyword_similarity_score.result_list_def;

  return (
    <>
      <h1>Semantics Analysis</h1>

      <Grid container spacing={3}>
        <Grid item xs>
          <Box className="speech-keywords-box">
            <h2>Speech Keywords</h2>
            <p>Significance of Speech Keywords</p>
            <div style={{ height: "460px" }}>
              <Grid
                container
                rowSpacing={1}
                columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                alignItems="center"
              >
                {speechKeywords.map(([keyword, value]: [string, number], index: number) => (
                  <React.Fragment key={index}>
                    <Grid item xs={6}>
                      <h3>{keyword}</h3>
                    </Grid>
                    <Grid item xs={6}>
                      <h3 className="percent-bg-sa">{value}</h3>
                    </Grid>
                  </React.Fragment>
                ))}
              </Grid>
            </div>
          </Box>
        </Grid>

        <Grid item xs={6}>
          <Box className="keywords-similarity-box">
            <h2>Speech and Lyrics Keywords Similarity</h2>
            <p>Similarity between keywords of speech audio and lyrics</p>
            <div style={{ height: "450px", marginLeft: "30px" }}>
              <MyResponsiveHeatMap
                data={keywordsSimilarity}
              />
            </div>
          </Box>
        </Grid>
        <Grid item xs>
          <Box className="lyrics-keywords-box">
            <h2>Lyrics Keywords</h2>
            <p>Significance of Lyrics Keywords</p>
            <div style={{ height: "460px" }}>
              <Grid
                container
                rowSpacing={1}
                columnSpacing={{ xs: 1, sm: 2, md: 3 }}
                alignItems="center"
              >
                {lyricsKeywords.map(([keyword, value]: [string, number], index: number) => (
                  <React.Fragment key={index}>
                    <Grid item xs={6}>
                      <h3>{keyword}</h3>
                    </Grid>
                    <Grid item xs={6}>
                      <h3 className="percent-bg-sa">{value}</h3>
                    </Grid>
                  </React.Fragment>
                ))}
              </Grid>
            </div>
          </Box>
        </Grid>
      </Grid>
    </>
  );
};

export default SemanticsAnalysis;
