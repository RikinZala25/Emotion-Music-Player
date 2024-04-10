import { ResponsiveHeatMap } from "@nivo/heatmap";

interface HeatMapData {
  id: string;
  data: any;
}

interface MyResponsiveHeatMapProps {
  data: HeatMapData[];
}

const MyResponsiveHeatMap: React.FC<MyResponsiveHeatMapProps> = ({ data }) => {

  const formattedData = data.map((item) => ({
    id: item.id,
    data: item.data.map((point: { x: any; y: number; }) => ({
      x: point.x,
      y: (Math.round(point.y * 10000) /100).toFixed(2),
    })),
  }));

  const getMaxValue = formattedData.reduce((acc, item) => {
    const itemMax = item.data.reduce((maxValue: number, point: { y: string; }) => {
      return Math.max(maxValue, parseFloat(point.y));
    }, 0);
    const tensValue = Math.ceil(itemMax / 10) * 10;

    return Math.max(acc, tensValue);
  }, 0);
  
  return (
    <ResponsiveHeatMap
      data={formattedData}
      margin={{ top: 60, right: 90, bottom: 60, left: 90 }}
      axisTop={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: -30,
        legend: "Lyrics Keywords",
        legendPosition: "middle",
        legendOffset: -50,
        truncateTickAt: 0,
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: "Speech Keywords",
        legendPosition: "middle",
        legendOffset: -72,
        truncateTickAt: 0,
      }}
      colors={{
        type: 'sequential',
        scheme: 'blues',
        minValue: 0,
        maxValue: getMaxValue,
      }}
      emptyColor="#555555"
      theme={{
        text: {
          fill: "#ffffff",
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
      labelTextColor="white"
      legends={[
        {
          anchor: "bottom",
          translateX: 0,
          translateY: 30,
          length: 400,
          thickness: 8,
          direction: "row",
          tickPosition: "after",
          tickSize: 3,
          tickSpacing: 4,
          tickOverlap: false,
          tickFormat: ">-.2s",
          title: "Value →",
          titleAlign: "start",
          titleOffset: 4,
        },
      ]}
    />
  );
};

export default MyResponsiveHeatMap;
