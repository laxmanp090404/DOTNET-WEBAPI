import { BehaviorSubject } from "rxjs";
import { UserModel } from "../models/user.model";

const readUserFromToken = () => {
    const token = sessionStorage.getItem('token');

    if (!token) {
        return null;
    }

    const payload = JSON.parse(atob(token.split('.')[1]));
    console.log("Decoded token payload:", payload);
    return new UserModel(
        payload.username ,
        payload.email,
        payload.gender,
        payload.firstName,
        payload.lastName,
        payload.image
    );
};

export const userSubject = new BehaviorSubject<UserModel | null>(readUserFromToken());
export const logoutUser = () => {
    sessionStorage.removeItem('token');
    userSubject.next(null);
    // console.log("User logged out, token removed from sessionStorage.");
};


export const isLoggedIn = () => {
    return sessionStorage.getItem('token') != null;
};

export const changeUser = () => {
    const user = readUserFromToken();

    if (user) {
        userSubject.next(user);
        // console.log("User updated to:", user);
    }
};