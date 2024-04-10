import { ResponsiveRadar } from "@nivo/radar";

interface RadarData {
  label: string;
  value: number;
  [key: string]: string | number;
}

interface MyResponsiveRadarProps {
  data: RadarData[];
}

const MyResponsiveRadar: React.FC<MyResponsiveRadarProps> = ({ data }) => (
  <ResponsiveRadar
    data={data}
    keys={["value"]}
    indexBy="label"
    valueFormat=">-.2f"
    maxValue={100}
    margin={{ top: 50, right: 100, left: 100 }}
    borderColor={{ from: "color" }}
    gridLabelOffset={36}
    dotSize={6}
    dotColor="#FF8E8F"
    dotBorderWidth={2}
    colors={["#FFB38E"]}
    motionConfig="wobbly"
    fillOpacity={0.8}
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
  />
);

export default MyResponsiveRadar;
