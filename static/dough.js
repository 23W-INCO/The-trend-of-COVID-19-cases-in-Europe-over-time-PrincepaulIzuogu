// Load the FHIR data from the JSON file
d3.json("static/processed_fhir.json").then(fhirData => {
  console.log(fhirData);  // Log the loaded data to the console

  const countryCounts = {};

  fhirData.forEach(immunization => {
      const patientReference = immunization.patient.reference;
      const country = patientReference.split('/').pop();

      if (!countryCounts[country]) {
          countryCounts[country] = 0;
      }
      countryCounts[country]++;
  });

  // Now countryCounts contains the counts of each country
  console.log(countryCounts);

  // Create a doughnut chart with the country counts
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

  const pie = d3.pie().value(d => d.value);
  const arc = d3.arc().innerRadius(radius * 0.6).outerRadius(radius);

  const dataForChart = Object.entries(countryCounts).map(([country, count]) => ({ country, value: count }));

  const arcs = svg.selectAll(".arc")
      .data(pie(dataForChart))
      .enter()
      .append("g")
      .attr("class", "arc");

  arcs.append("path")
      .attr("d", arc)
      .attr("fill", (d, i) => colorScale(i));

  // Display the country labels
  arcs.append("text")
      .attr("transform", d => `translate(${arc.centroid(d)})`)
      .attr("text-anchor", "middle")
      .text(d => `${d.data.country}: ${d.data.value}`);
});
