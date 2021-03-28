const express = require("express");
const Firestore = require("@google-cloud/firestore");

const db = new Firestore();
const app = express();
app.use(express.json());

app.get("/", (req, res) => {
  const name = process.env.NAME || "ESP32";
  res.send(`Welcome into ${name} Weather Station API!`);
});

app.get("/weather/:placeId", async (req, res) => {
  const placeId = req.params.placeId;
  const query = db.collection("weather-data").where("placeId", "==", placeId);
  const querySnapshot = await query.get();
  if (querySnapshot.size > 0) {
    res.json(querySnapshot.docs);
  } else {
    res.status(404).json({ status: `${placeID} not Found` });
  }
});

app.post("/weather", async (req, res) => {
  const data = {
    temperature: req.body.temperature,
    humidity: req.body.humidity,
    pressure: req.body.pressure,
    placeId: req.body.placeId,
  };
  // .doc() creates a new document, .set() sets the data into it
  await db.collection("weather-data").doc().set(data);
  // res.status(200).json({ ...data });
  res.statusCode(200); // to send only status code without any data
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Weather API: listening on port ${port}`);
});
