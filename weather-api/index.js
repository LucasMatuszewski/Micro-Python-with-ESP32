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
  // if (querySnapshot.exists) { // why it doesn't work?
  if (querySnapshot.size > 0) {
    // .docs are not simple objects, they contains also prototypes, metadata & timestamps
    // We iterate every doc.data() to retrieve all fields in the document as an simple Object.
    const weatherData = querySnapshot.docs.map((doc) => doc.data());
    res.status(200).json(weatherData);
  } else {
    res.status(404).json({ status: `Data not Found` });
  }
});

app.get("/weather/place/:placeId", async (req, res) => {
  const placeId = req.params.placeId;
  const query = weatherDb.where("placeId", "==", placeId);
  const querySnapshot = await query.get();
  if (querySnapshot.size > 0) {
    const weatherData = querySnapshot.docs.map((doc) => doc.data());
    res.status(200).json(weatherData);
  } else {
    res.status(404).json({ status: `Weather data for ${placeId} not Found` });
  }
});

app.post("/weather", async (req, res) => {
  // To store Secrets we can use Secret Manager: https://cloud.google.com/build/docs/securing-builds/use-secrets
  // It works on triggered Build Time but it's not available in free tier?
  // We can use for free this solution:
  // https://stackoverflow.com/questions/52840187/how-to-set-environment-variables-using-google-cloud-build-or-other-method-in-goo

  // Or we can add variables manually adding new revision: https://cloud.google.com/run/docs/configuring/environment-variables#console
  if (req.body.secretApiKey === process.env.API_KEY) {
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
    res.sendStatus(200); // to send only status code with automate .send('OK')
  } else {
    res.sendStatus(403); // to send only status code with automate .send('Forbidden')
  }
});

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Weather API: listening on port ${port}`);
});
