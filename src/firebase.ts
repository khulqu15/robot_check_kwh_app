// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBhFKQ73tsHA7ZFQnel2D7tuUkHNHie1ug",
  authDomain: "kwhmeter-d9fda.firebaseapp.com",
  databaseURL: "https://kwhmeter-d9fda-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "kwhmeter-d9fda",
  storageBucket: "kwhmeter-d9fda.appspot.com",
  messagingSenderId: "539756566253",
  appId: "1:539756566253:web:c18ecd52b0a7bc82b8dee4",
  measurementId: "G-JL73R0L5BT"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const database = getDatabase(app);
export { app, analytics, auth, database };
