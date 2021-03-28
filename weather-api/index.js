const express = require("express");
// library with functions to work only with Firestore:
const Firestore = require("@google-cloud/firestore");
// documentation: https://googleapis.dev/nodejs/firestore/2.2.3/index.html

// SDK to work with whole Firebase ecosystem:
// const admin = require('firebase-admin');
// admin.initializeApp({
//   credential: admin.credential.cert(serviceAccount)
// });
// const db = admin.firestore();

// Firestore queries docs: https://firebase.google.com/docs/firestore/query-data/order-limit-data

const db = new Firestore();
const app = express();
app.use(express.json());

app.get("/", (req, res) => {
  const name = process.env.NAME || "ESP32";
  res.send(`Welcome into ${name} Weather Station API!`);
});

const weatherDb = db.collection("weather-data");

app.get("/weather/limit/:limit", async (req, res) => {
  const limit = parseInt(req.params.limit);
  const query = weatherDb.limit(limit);
  const querySnapshot = await query.get();
  // if (querySnapshot.size > 0) {
  if (querySnapshot.exists) {
    res.status(200).json(querySnapshot.docs);
  } else {
    res.status(404).json({ status: `${placeID} not Found` });
  }
});

app.get("/weather/place/:placeId", async (req, res) => {
  const placeId = req.params.placeId;
  const query = weatherDb.where("placeId", "==", placeId);
  const querySnapshot = await query.get();
  if (querySnapshot.exists) {
    res.status(200).json(querySnapshot.docs);
    console.log("querySnapshot.docs", querySnapshot.docs);
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
    created: Firestore.Timestamp.now(),
  };
  // .doc() creates a new document with default random ID or we can specify a name for it .doc('docname')
  // .set() sets the data into it
  await weatherDb.doc().set(data);
  // res.status(200).json({ ...data });
  res.statusCode(200); // to send only status code without any data
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Weather API: listening on port ${port}`);
});
