import React, { useState } from "react";
import axios from "axios";
// import { AxiosResponse } from "axios";
import { useAudioRecorder } from "@sarafhbk/react-audio-recorder";

// Material UI
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import { Button } from "@mui/material";
import { styled } from "@mui/material/styles";

// React Icons
import { IoIosMusicalNote } from "react-icons/io";
import { PiMusicNotesPlus } from "react-icons/pi";
import { FaCloudUploadAlt, FaExternalLinkAlt } from "react-icons/fa";

// Custom Containers
import OutputBoxRenderer from "./Components/outputBoxRenderer";
import DisplayResult from "./Components/displayResults";

// Custom CSS
import "./App.css";

interface MainAppProps {}

interface ResponseData {
  text_va: Record<string, any>;
  audio_emotion: Record<string, any>;
  detected_text: string;
  suggested_songs: any[];
  final_prediction: Record<string, any>;
  input_text_keywords: any[];
  emotion_quadrant_angle: Record<string, any>;
  text_emotion_confidence: any[];
}

interface GeneratedSong {
  va_value: string;
  generated_song: string;
}

const MainApp: React.FC<MainAppProps> = () => {
  const [showMoreInfo, setShowMoreInfo] = useState(false);
  const [moreInfoData, setMoreInfoData] = useState<any>(null);
  const [data, setData] = useState<ResponseData | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingStarted, setRecordingStarted] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [generatedSongUrl, setGeneratedSongUrl] =
    useState<GeneratedSong | null>(null);
  const { audioResult, startRecording, stopRecording } = useAudioRecorder();

  // Setup your base url
  // const BASE_URL = "https://01fa-34-30-42-155.ngrok-free.app";

  const handleClick = (data: any) => {
    setShowMoreInfo(true);
    setMoreInfoData(data);
  };

  const handleCloseClick = () => {
    setShowMoreInfo(false);
  };

  const handleRecommendMusic = async () => {
    if (!selectedFile && !audioResult) {
      window.alert("Please select any Audio file or Record Audio.");
      return;
    }

    const formData = new FormData();

    if (audioResult && audioResult.startsWith("blob:")) {
      const blobResponse = await fetch(audioResult);
      const blobData = await blobResponse.blob();
      formData.append("audio_file", blobData, "audio_recording.wav");
    } else {
      formData.append("audio_file", selectedFile || "");
    }

    try {
      
      // Setup the recommend_music api
      // const response: AxiosResponse<ResponseData> = await axios.post(
      //   `${BASE_URL}/recommend_music`,
      //   formData,
      //   {
      //     headers: {
      //       "Content-Type": "multipart/form-data",
      //     },
      //   }
      // );

      const response = await axios.get(
        "https://api.npoint.io/c15dbe45337732f514fc"
      );

      setData(response.data);
    } catch (error) {
      console.error("Error recommending music:", error);
    }
  };

  const VisuallyHiddenInput = styled("input")({
    clip: "rect(0 0 0 0)",
    clipPath: "inset(50%)",
    height: 1,
    overflow: "hidden",
    position: "absolute",
    bottom: 0,
    left: 0,
    whiteSpace: "nowrap",
    width: 1,
  });

  const handleMicrophoneClick = () => {
    if (!recordingStarted) {
      startRecording();
      setIsRecording(true);
      setRecordingStarted(true);
      document.body.classList.add("recording-started");
    } else {
      stopRecording();
      setIsRecording(false);
      setRecordingStarted(false);
      document.body.classList.remove("recording-started");
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setSelectedFile(file || null);
  };

  const renderOutputBoxes = () => {
    if (!data || !data.suggested_songs) return null;

    return data.suggested_songs.map((song, index) => (
      <OutputBoxRenderer
        showMusicPercentDiv={true}
        displayData={song}
        key={index}
        handleClick={handleClick}
      />
    ));
  };

  let detectedEmotion = "";

  if (data && data.final_prediction) {
    detectedEmotion = `${data.final_prediction.label} : ${(
      Math.round(data.final_prediction.value * 10000) / 100
    ).toFixed(2)} %`;
  } else {
    detectedEmotion = "Data unavailable";
  }

  const handleGenerateMusic = async () => {
    if (!data || !data.final_prediction || !data.final_prediction.label) {
      window.alert("You will get Recommendations and Generated Music as well.");
      handleRecommendMusic();
    }

    data && console.log("Emotion: ", data.final_prediction.label);

    const formData = new FormData();
    data && formData.append("emotion", data.final_prediction.label);

    try {
      
      // Setup the generate_audio_music api
      // const response = await axios.post(
      //   `${BASE_URL}/generate_audio_music`,
      //   formData,
      //   {
      //     headers: {
      //       "Content-Type": "multipart/form-data",
      //     },
      //   }
      // );

      const response = await axios.get(
        "https://api.npoint.io/db551465651f6bb08535"
      );

      const generatedSongUrlFromResponse = response.data;
      setGeneratedSongUrl(generatedSongUrlFromResponse);
    } catch (error) {
      console.error("Error generating music:", error);
    }
  };

  return (
    <>
      <div className="main_title">
        <h1>SoulSyncopia: Emotion-Based Music Recommendation System</h1>
      </div>

      <React.Fragment>
        <Container maxWidth="xl" fixed>
          <Grid container>
            <Grid item xs={4}>
              <div className="left-container">
                <Box className="custom-box input-box">
                  <div className="audio-input-container">
                    <div className="audio-input-wrapper">
                      <div className="controls" data-role="controls">
                        <button
                          className={isRecording ? "recording" : "none"}
                          onClick={handleMicrophoneClick}
                        >
                          {isRecording ? "Stop Recording" : "Start Recording"}
                        </button>
                      </div>
                    </div>
                    <p style={{paddingRight: '10px'}}>Or</p>
                    <Button
                      component="label"
                      role={undefined}
                      variant="contained"
                      tabIndex={-1}
                      startIcon={<FaCloudUploadAlt />}
                    >
                      Upload file
                      <VisuallyHiddenInput
                        type="file"
                        accept=".mp3,.wav"
                        onChange={handleFileUpload}
                      />
                    </Button>
                  </div>
                  <audio
                    className="audio-output"
                    controls
                    src={
                      selectedFile
                        ? URL.createObjectURL(selectedFile)
                        : audioResult
                    }
                  />

                  <Button
                    variant="contained"
                    className="recommendMusicButton"
                    style={{ width: "90%", marginTop: "70px" }}
                    onClick={handleRecommendMusic}
                  >
                    <IoIosMusicalNote /> &nbsp; Recommend Music
                  </Button>
                  <br />
                  <br />
                  <Button
                    variant="contained"
                    className="generateMusicButton"
                    style={{
                      width: "90%",
                      cursor:
                        !data ||
                        !data.final_prediction ||
                        !data.final_prediction.label
                          ? "not-allowed"
                          : "pointer",
                    }}
                    onClick={handleGenerateMusic}
                  >
                    <PiMusicNotesPlus /> &nbsp; Generate Music
                  </Button>
                </Box>
                {data && (
                  <Box className="custom-box result-box">
                    <h2 className="genenerated-emotion">Your Emotion</h2>
                    <h2 className="genenerated-emotion-label">
                      {detectedEmotion}
                    </h2>
                  </Box>
                )}
              </div>
            </Grid>

            <Grid item xs={8}>
              <Box
                className="custom-box output-box"
                style={{ marginLeft: showMoreInfo ? "-70px" : "-60px" }}
              >
                {data && renderOutputBoxes()}
              </Box>
            </Grid>
          </Grid>
        </Container>

        {showMoreInfo && (
          <>
            <Container maxWidth="xl" fixed>
              <Box className="custom-box more-info-box">
                <Box className="more-info-btn-box">
                  <h3>More Info</h3>
                </Box>
                <DisplayResult
                  displayResultData={data}
                  displayDetectedEmotion={detectedEmotion}
                  selectedSongData={moreInfoData}
                />
                <a onClick={handleCloseClick}>
                  <Box className="close-info-box">
                    <h3>Close Info</h3>
                  </Box>
                </a>
              </Box>
            </Container>
          </>
        )}

        {generatedSongUrl && data && (
          <>
            <Container maxWidth="xl" fixed>
              <Box className="custom-box more-info-box" style={{width: '101%'}}>
                <Box className="more-info-btn-box">
                  <h3>Generated Music</h3>
                </Box>

                <h1>
                  Music Generation By :&nbsp;
                  <a
                    className="generation-box"
                    href="https://replicate.com/annahung31/emopia"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    EMOPIA <FaExternalLinkAlt />
                  </a>
                </h1>
                <h2>Predicted Emotion : {data.final_prediction.label}</h2>
                <h2>VA : {generatedSongUrl.va_value}</h2>

                <audio
                  controls
                  style={{ width: "50%" }}
                  onError={(e) => console.log("Audio Error:", e)}
                >
                  <source
                    src={generatedSongUrl.generated_song}
                    type="audio/mpeg"
                  />
                </audio>
                <br />
                <br />
                <Box className="more-info-btn-box">
                  <br />
                </Box>
              </Box>
            </Container>
          </>
        )}
      </React.Fragment>
    </>
  );
};

export default MainApp;
