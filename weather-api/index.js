const express = require("express");
const app = express();

app.get("/", (req, res) => {
  const name = process.env.NAME || "ESP32";
  res.send(`Hello ${name}!`);
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Weather API: listening on port ${port}`);
});
