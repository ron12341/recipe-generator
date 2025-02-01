// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDl7R0-zZEzmub4JGH3S-fvdA4fouYIHyU",
  authDomain: "recipe-generator-ad527.firebaseapp.com",
  projectId: "recipe-generator-ad527",
  storageBucket: "recipe-generator-ad527.firebasestorage.app",
  messagingSenderId: "539241987973",
  appId: "1:539241987973:web:cf8993c474dfc5f4344eec",
  measurementId: "G-B9Z40YCVWV"
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
const analytics = getAnalytics(firebaseApp);

export { firebaseApp, analytics };