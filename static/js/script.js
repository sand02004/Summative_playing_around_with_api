document.getElementById("searchBtn").addEventListener("click", function () {
  const query = document.getElementById("searchInput").value.trim();

  if (!query) {
    document.getElementById("results").innerHTML = "<p>Please enter a search term.</p>";
    return;
  }

  const apiUrl = `https://health.gov/myhealthfinder/api/v3/topicsearch.json?keyword=${encodeURIComponent(query)}`;

  fetch(apiUrl)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      const results = document.getElementById("results");
      results.innerHTML = "";

      const topics = data.Result?.Resources?.Resource;

      if (!topics || topics.length === 0) {
        results.innerHTML = "<p>No tips found for that topic.</p>";
        return;
      }

      topics.forEach((tip) => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
          <h3>${tip.Title}</h3>
          <p>${tip.Description}</p>
          <a href="${tip.AccessibleVersion}" target="_blank">Read more</a>
        `;
        results.appendChild(card);
      });
    })
    .catch((error) => {
      document.getElementById("results").innerHTML = "<p>Error fetching data. Please try again later.</p>";
      console.error("Fetch error:", error);
    });
});