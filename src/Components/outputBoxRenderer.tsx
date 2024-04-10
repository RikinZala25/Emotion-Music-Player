import React, { useState, useRef, useEffect } from "react";
import { Grid, Container, Box, Button } from "@mui/material";
import { FaSpotify, FaPlayCircle, FaPauseCircle } from "react-icons/fa";
import "./css/outputBoxRenderer.css";

interface Props {
  showMusicPercentDiv: boolean;
  displayData: any;
  handleClick: (data: any) => void;
}

const OutputBoxRenderer: React.FC<Props> = ({
  showMusicPercentDiv,
  displayData,
  handleClick,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);

  const [bgColor, setBgColor] = useState("#247881"); // Initial background color
  const colors = [
    "#247881",
    "#0B666A",
    "#836FFF",
    "#FB6D48",
    "#6420AA",
    "#FF204E",
    "#61677A",
    "#607274",
  ];

  const imageLink = displayData.images[2].url;

  const previewUrl = displayData.preview_url;

  const audioLink = displayData.track_url;

  const overallSimilarity = displayData.overall_similarity.toFixed(2);

  let artistsString = displayData.artists.join(", ");

  let songString = displayData.name;

  let maxCharacters = 80;

  if (artistsString.length > maxCharacters) {
    artistsString = artistsString.substring(0, maxCharacters - 3) + "...";
  }

  if (songString.length > maxCharacters) {
    songString = songString.substring(0, maxCharacters - 3) + "...";
  }

  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    const randomIndex = Math.floor(Math.random() * colors.length);
    setBgColor(colors[randomIndex]);
  }, []);

  const handlePlayPauseClick = () => {
    if (isPlaying) {
      audioRef.current?.pause();
    } else {
      audioRef.current?.play();
    }
    setIsPlaying((prevState) => !prevState);
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
  };

  const boxStyle = {
    backgroundColor: bgColor,
    width: "106%",
  };

  const handleButtonClick = () => {
    handleClick(displayData);
  };

  return (
    <div className="output-box-inner-div">
      <Grid item xs={10}>
        <Container className="output-box-container">
          <Box className="output-box-music-div" style={boxStyle}>
            <div className="output-box-music-inner-div">
              <img src={imageLink} className="music-image" />

              <div className="output-box-music-inner-div-content">
                <h3>{songString}</h3>
                <p>{artistsString}</p>
                <p className="preview-btn-p">
                  <span className="preview-btn">PREVIEW</span>
                </p>
              </div>
            </div>

            <div className="output-box-music-inner-div-right">
              <a
                href={audioLink}
                target="_blank"
                rel="noopener noreferrer"
                className="spotify-icon-link"
              >
                <FaSpotify className="spotify-icon" />
              </a>
              <br /> <br />
              {isPlaying ? (
                <FaPauseCircle
                  className="play-song-icon"
                  onClick={handlePlayPauseClick}
                />
              ) : (
                <FaPlayCircle
                  className="play-song-icon"
                  onClick={handlePlayPauseClick}
                />
              )}
            </div>
          </Box>
        </Container>
      </Grid>
      <Grid item xs={2}>
        {showMusicPercentDiv && (
          <div className="output-box-music-percent-div">
            <h3>{overallSimilarity} %</h3>
            <Button
              variant="contained"
              className="submitButton"
              onClick={handleButtonClick}
            >
              More
            </Button>
          </div>
        )}
      </Grid>

      <div style={{ display: "none" }}>
        <audio ref={audioRef} src={previewUrl} onEnded={handleAudioEnded} />
      </div>
    </div>
  );
};

export default OutputBoxRenderer;
