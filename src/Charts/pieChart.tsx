import { ResponsivePie } from "@nivo/pie";

interface PieData {
  label: string;
  value: number;
}

interface MyResponsivePieProps {
  data: PieData[];
}

const MyResponsivePie: React.FC<MyResponsivePieProps> = ({ data }) => {

  const getColorForLabel = (label: string): string => {
    switch (label.toLowerCase()) {
      case "anger":
        return "hsl(273, 70%, 50%)";
      case "calmness":
        return "hsl(267, 70%, 50%)";
      case "happiness":
        return "hsl(337, 70%, 50%)";
      case "sadness":
        return "hsl(216, 70%, 50%)";
      default:
        return "hsl(187, 70%, 50%)";
    }
  };

  const formattedData = data.map((item) => ({
    label: item.label,
    value: (Math.round(item.value * 10000) / 100).toFixed(2),
    id: item.label,
    color: getColorForLabel(item.label),
  }));

  return (
    <ResponsivePie
      data={formattedData}
      margin={{ top: 10, right: 80, bottom: 80, left: 100 }}
      innerRadius={0.5}
      padAngle={0.7}
      cornerRadius={3}
      activeOuterRadiusOffset={8}
      borderWidth={1}
      borderColor={{
        from: "color",
        modifiers: [["darker", 0.2]],
      }}
      enableArcLinkLabels={false}
      arcLinkLabelsSkipAngle={10}
      arcLinkLabelsTextColor="#ffffff"
      arcLinkLabelsThickness={2}
      arcLinkLabelsColor={{ from: "color" }}
      arcLabelsSkipAngle={10}
      arcLabelsTextColor="white"
      theme={{
        text: {
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
          anchor: "bottom",
          direction: "row",
          justify: false,
          translateX: 0,
          translateY: 56,
          itemsSpacing: 0,
          itemWidth: 100,
          itemHeight: 18,
          itemTextColor: 'white',
          itemDirection: "left-to-right",
          itemOpacity: 1,
          symbolSize: 18,
          symbolShape: "circle",
        },
      ]}
    />
  );
};

export default MyResponsivePie;
