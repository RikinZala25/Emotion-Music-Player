import { ResponsiveScatterPlotCanvas } from "@nivo/scatterplot";

interface ScatterPlotData {
  id: string;
  data: any;
}

interface MyResponsiveScatterPlotProps {
  data: ScatterPlotData[];
}

const MyResponsiveScatterPlot: React.FC<MyResponsiveScatterPlotProps> = ({
  data,
}) => (
  <ResponsiveScatterPlotCanvas
    data={data}
    margin={{ top: 30, right: 170, bottom: 70, left: 90 }}
    xScale={{ type: "linear", min: -1, max: 1 }}
    xFormat=">-.2f"
    yScale={{ type: "linear", min: -1, max: 1 }}
    yFormat=">-.2f"
    axisTop={null}
    axisRight={null}
    axisBottom={{
      //   orient: "bottom",
      tickSize: 5,
      tickPadding: 5,
      tickRotation: 0,
      legend: "valence",
      legendPosition: "middle",
      legendOffset: 46,
      truncateTickAt: 0,
    }}
    axisLeft={{
      //   orient: "left",
      tickSize: 5,
      tickPadding: 5,
      tickRotation: 0,
      legend: "arousal",
      legendPosition: "middle",
      legendOffset: -60,
      truncateTickAt: 0,
    }}
    theme={{
      text: {
        fill: "white",
        fontSize: 12,
        fontWeight: "bolder",
      },
      tooltip: {
        container: {
          backgroundColor: "black",
          borderRadius: "5px",
        },
      },
      legends: {
        text: {
          fontSize: 12,
          fontWeight: "bolder",
        },
      },
    }}
    legends={[
      {
        itemTextColor: "white",
        anchor: "right",
        direction: "column",
        justify: false,
        translateX: 130,
        translateY: 0,
        itemWidth: 100,
        itemHeight: 12,
        itemsSpacing: 5,
        itemDirection: "left-to-right",
        symbolSize: 12,
        symbolShape: "circle",
        effects: [
          {
            on: "hover",
            style: {
              itemOpacity: 1,
            },
          },
        ],
      },
    ]}
  />
);

export default MyResponsiveScatterPlot;
