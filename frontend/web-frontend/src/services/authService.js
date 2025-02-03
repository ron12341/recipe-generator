import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';
import axios from 'axios';
import { firebaseApp } from './firebase';

export const signupUser = async (email, password) => {
    const auth = getAuth();
    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Get the Firebase ID Token
        const idToken = await user.getIdToken(true);

        console.log("ID TOKEN: ", idToken);

        // Send the token to the backend for verification
        const response = await axios.post('http://localhost:8000/auth/signup', {
            id_token: idToken,
            email: email
        });

        console.log("RESPONSE: ", response);
        console.log("RESPONSE DATA: ", response.data);

        return response.data;

    } catch (error) {
        if (error.code === 'auth/email-already-in-use') {
            console.error('Email already in use');
            return { error: 'Email already in use' };
        } else {
            console.error('Error signing up user:', error);
            if (error.response) {
                console.log("STATUS CODE: ", error.response.status);
                console.log("ERROR MESSAGE: ", error.response.data);
            }
            throw error;
        }
    }
};

export const loginUser = async (email, password) => {
    const auth = getAuth();
    try {

        console.log("LOGGING IN USER");
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        const idToken = await user.getIdToken();

        console.log("ID TOKEN: ", idToken);

        const response = await axios.post('http://localhost:8000/auth/login', {
            id_token: idToken,
            email: email
        });

        console.log("RESPONSE: ", response);

        if (response.status === 200) {
            return response.data;
        } else {
            throw new Error('Login failed');
        }

    } catch (error) {
        console.error('Error signing in user:', error);
        throw error;
    }
};

export const logoutUser = async () => {
    try {
        await firebaseApp.auth().signOut();
    } catch (error) {
        console.error('Error logging out user:', error);
        throw error;
    }
};