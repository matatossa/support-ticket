import { initializeApp } from "firebase/app";
import { getAuth, signInWithPhoneNumber, RecaptchaVerifier } from "firebase/auth";

// Firebase configuration with your project credentials
const firebaseConfig = {
  apiKey: "AIzaSyAlIicDm35DqJ-oGVf5wp62fO7IrZKXZ_Q",
  authDomain: "number-verification-1a568.firebaseapp.com",
  projectId: "number-verification-1a568",
  storageBucket: "number-verification-1a568.appspot.com",
  messagingSenderId: "903833155955",
  appId: "1:903833155955:web:dc865f45a74eaa455b2d06",
  measurementId: "G-WM0NRLRKVS"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Set up reCAPTCHA (invisible)
window.recaptchaVerifier = new RecaptchaVerifier('phone-form', {
    'size': 'invisible',
    'callback': function(response) {
        // reCAPTCHA solved automatically when the user submits the form
        console.log('reCAPTCHA solved');
    },
    'expired-callback': function() {
        // Response expired. Ask user to solve reCAPTCHA again
        console.error('reCAPTCHA expired, try again');
    }
}, auth);

// Send OTP (Phone Number Verification)
document.getElementById('phone-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const phoneNumber = document.getElementById('phone-number').value;
    const appVerifier = window.recaptchaVerifier;

    signInWithPhoneNumber(auth, phoneNumber, appVerifier)
        .then(function(confirmationResult) {
            // Successfully sent OTP, hide phone form and show verification form
            window.confirmationResult = confirmationResult;
            document.getElementById('phone-form').style.display = 'none';
            document.getElementById('verification-form').style.display = 'block';
            console.log('OTP sent');
        })
        .catch(function(error) {
            console.error("Error sending OTP: ", error);
            // Optionally show the error to the user
        });
});

// Verify OTP (User enters the verification code)
document.getElementById('verification-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const verificationCode = document.getElementById('verification-code').value;

    window.confirmationResult.confirm(verificationCode)
        .then(function(result) {
            // OTP verification successful
            console.log("Phone number verified successfully!");
            
            // Redirect to Django success view
            window.location.href = '/accounts/verify_phone_success/';
        })
        .catch(function(error) {
            console.error("Error verifying OTP: ", error);
            // Optionally show the error to the user
        });
});
