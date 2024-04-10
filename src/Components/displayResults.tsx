import React from "react";
import SemanticsAnalysis from "../Components/semanticsAnalysis";
import TextLyricsAnalysis from "../Components/textLyricsAnalysis";
import AudioAcousticsAnalysis from "../Components/audioAcousticsAnalysis";
import OverallAnalysis from "../Components/overallAnalysis";

interface Props {
  displayResultData: any;
  selectedSongData: any;
  displayDetectedEmotion: string;
}

const DisplayResult: React.FC<Props> = ({ displayResultData, selectedSongData, displayDetectedEmotion }) => {
  
  return (
    <>
      {/* Display Overall Analysis */}
      <OverallAnalysis selectedSongData={selectedSongData} displayDetectedEmotion={displayDetectedEmotion} />

      {/* Display Audio Lyrics Analysis */}
      <AudioAcousticsAnalysis displayResultData={displayResultData} selectedSongData={selectedSongData} />

      {/* Display Text Lyrics Analysis */}
      <TextLyricsAnalysis displayResultData={displayResultData} selectedSongData={selectedSongData} />

      {/* Display Semantics Analysis */}
      <SemanticsAnalysis displayResultData={displayResultData} selectedSongData={selectedSongData} />
    </>
  );
};

export default DisplayResult;
