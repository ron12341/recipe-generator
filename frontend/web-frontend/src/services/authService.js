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

        // Send the token to the backend for verification
        const response = await axios.post('http://localhost:8000/auth/signup', {
            id_token: idToken,
            email: email
        });

        if (response.status === 200) {
            console.log('User signed up successfully');
        } else {
            throw new Error(response.data.detail || 'Signup failed');
        }

    } catch (error) {
        console.error('Error signing up user:', error);
        throw error;
    }
};

export const loginUser = async (email, password) => {
    const auth = getAuth();
    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        const token = await user.getIdToken();

        // Send the token to the backend for verification
        const response = await fetch('http://localhost:8080/user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.ok) {
            const data = await response.json();
            return data;
        } else {
            throw new Error('User not found');
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