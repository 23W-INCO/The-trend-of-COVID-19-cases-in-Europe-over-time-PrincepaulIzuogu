// Load the data from the JSON file
d3.json("/static/data.json").then(data => {
    

    // Set up the initial doughnut chart
    const width = 200;
    const height = 200;
    const radius = Math.min(width, height) / 2;

    const svg = d3.select("#dough-container")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const colorScale = d3.scaleOrdinal(d3.schemeCategory10);

    // Calculate the total vaccinations for each location from 2021 to 2023
    const totalVaccinationsByLocation = {};

    data.forEach(entry => {
      const year = new Date(entry.date).getFullYear();
      if (year >= 2021 && year <= 2023) {
        if (!totalVaccinationsByLocation[entry.location]) {
          totalVaccinationsByLocation[entry.location] = 0;
        }
        totalVaccinationsByLocation[entry.location] += entry.total_vaccinations;
      }
    });

    // Calculate the total vaccinations across all locations
    const totalVaccinations = d3.sum(Object.values(totalVaccinationsByLocation));

    // Calculate the percentage of total vaccinations for each location
    const percentageData = Object.entries(totalVaccinationsByLocation).map(([location, total]) => ({
      location,
      percentage: totalVaccinations > 0 ? total / totalVaccinations : 0,
      totalVaccinations: total
    }));

    // Sort the data based on the percentage
    const sortedData = percentageData.slice().sort((a, b) => b.percentage - a.percentage);

    // Create a function to update the chart based on the view mode
    function updateChart(isHigh) {
      // Select the top or bottom 5 entries based on the view mode
      const displayedData = isHigh ? sortedData.slice(0, 5) : sortedData
        .filter(entry => entry.totalVaccinations > 0)
        .slice(-5);

      // Create a new pie chart with the displayed data
      const pie = d3.pie().value(d => d.percentage);
      const arc = d3.arc().innerRadius(radius * 0.6).outerRadius(radius);

      // Clear existing elements
      svg.selectAll("*").remove();

      const arcs = svg.selectAll(".arc")
        .data(pie(displayedData));

      arcs.enter()
        .append("g")
        .attr("class", "arc")
        .append("path")
        .attr("d", arc)
        .attr("fill", (d, i) => colorScale(i))
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);
// Add labels with flags and percentages
const labelContainer = svg.selectAll(".label-container")
  .data(pie(displayedData));

const flagPath = d => `/flags/${d.data.location}.png`;  // Adjusted path for capitalization

labelContainer.enter()
  .append("g")
  .attr("class", "label-container")
  .append("image")
  .attr("xlink:href", flagPath)
  .attr("class", "flag country-flag") 
  .attr("x", d => arc.centroid(d)[0] - 15)
  .attr("y", d => arc.centroid(d)[1] - 10)
  .attr("width", 20)
  .attr("height", 15);

labelContainer.append("text")
  .text(d => `${d.data.location}\n${abbreviateNumber(d.data.totalVaccinations)} (${(d.data.percentage * 100).toFixed(2)}%)`)
  .attr("x", d => arc.centroid(d)[0] + 20)
  .attr("y", d => arc.centroid(d)[1] + 5)
  .attr("text-anchor", "start");
        
// Add percentages as separate labels
const percentageLabels = svg.selectAll(".percentage-label")
  .data(pie(displayedData));

percentageLabels.enter()
  .append("text")
  .text(d => `${(d.data.percentage * 100).toFixed(2)}%`)
  .attr("transform", d => `translate(${arc.centroid(d)})`)
  .attr("text-anchor", "middle")
  .attr("dy", 20) // Adjust vertical position
  .attr("class", "percentage-label");

    }

    // Function to handle mouseover events and display tooltips
    function handleMouseOver(d, i) {
      const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

      tooltip.transition()
        .duration(200)
        .style("opacity", .9);

      tooltip.html(`${d.data.location}\n${abbreviateNumber(d.data.totalVaccinations)} (${(d.data.percentage * 100).toFixed(2)}%)`)
        .style("left", (d3.event.pageX) + "px")
        .style("top", (d3.event.pageY - 28) + "px");
    }

    // Function to handle mouseout events and hide tooltips
    function handleMouseOut(d, i) {
      d3.select(".tooltip").transition()
        .duration(500)
        .style("opacity", 0)
        .remove();
    }

    // Toggle button event handler
    const toggleButton = document.getElementById("toggleButton");
    let isHigh = true;

    toggleButton.addEventListener("click", () => {
      isHigh = !isHigh;
      toggleButton.textContent = isHigh ? "See least locations" : "See high locations";
      updateChart(isHigh);
    });

    // Initialize the chart with the high 5 locations
    updateChart(true);
  });

  // Function to abbreviate large numbers
  function abbreviateNumber(value) {
    const suffixes = ["", "K", "M", "B", "T"];
    const tier = Math.log10(value) / 3 | 0;

    if (tier === 0) return value;

    const suffix = suffixes[tier];
    const scale = Math.pow(10, tier * 3);

    const scaledValue = value / scale;

    // Use 1 decimal place for values less than 10
    const formattedValue = scaledValue < 10 ? scaledValue.toFixed(1) : Math.round(scaledValue);

    return formattedValue + suffix;
  }
