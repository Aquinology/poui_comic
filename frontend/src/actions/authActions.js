import axios from 'axios';
import {
    SIGNUP_SUCCESS,
    SIGNUP_FAIL,
    ACTIVATION_SUCCESS,
    ACTIVATION_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    USER_LOADED_SUCCESS,
    USER_LOADED_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
    REFRESH_SUCCESS,
    REFRESH_FAIL,
    PASSWORD_RESET_SUCCESS,
    PASSWORD_RESET_FAIL,
    PASSWORD_RESET_CONFIRM_SUCCESS,
    PASSWORD_RESET_CONFIRM_FAIL,
    LOGOUT
} from '../types';


export const login = (username, password) => async dispatch => {

    const body = JSON.stringify({ username, password });

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {

        const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/auth/jwt/create/`, body, config);

        dispatch({
            type: LOGIN_SUCCESS,
            payload: response.data
        });

        dispatch(load_user());

    } catch (err) {

        dispatch({
            type: LOGIN_FAIL
        })

    }
};

export const load_user = () => async dispatch => {

    if (localStorage.getItem('access')) {

        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `JWT ${localStorage.getItem('access')}`,
                'Accept': 'application/json'
            }
        };

        try {

            const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/v1/auth/users/me/`, config);

            dispatch({
                type: USER_LOADED_SUCCESS,
                payload: response.data
            });

        } catch (err) {

            dispatch({
                type: USER_LOADED_FAIL
            });

        }
    } else {

        dispatch({
            type: USER_LOADED_FAIL
        });

    }
};

export const checkAuthenticated = () => async dispatch => {

    if (localStorage.getItem('access')) {

        const body = JSON.stringify({ token: localStorage.getItem('access') });

        const config = {
            headers: {
                'Content-Type': 'application/json'
            }
        };

        try {

            await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/auth/jwt/verify/`, body, config)

            dispatch({
                type: AUTHENTICATED_SUCCESS
            });

            dispatch(load_user());

        } catch (err) {

            dispatch({
                type: AUTHENTICATED_FAIL
            });

            dispatch(refresh());

        }

    } else {

        dispatch({
            type: AUTHENTICATED_FAIL
        });

    }
};

export const refresh = () => async dispatch => {

    if (localStorage.getItem('refresh')) {

        const body = JSON.stringify({ refresh: localStorage.getItem('refresh') });

        const config = {
            headers: {
                'Content-Type': 'application/json'
            }
        };

        try {

            const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/auth/jwt/refresh/`, body, config)

            dispatch({
                type: REFRESH_SUCCESS,
                payload: response.data
            });

            dispatch(load_user());

        } catch (err) {

            dispatch({
                type: REFRESH_FAIL
            });

        }

    } else {

        dispatch({
            type: REFRESH_FAIL
        });

    }
};

export const register = (email, username, password, re_password) => async dispatch => {

    const body = JSON.stringify({ email, username, password, re_password });

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {

        const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/auth/users/`, body, config);

        dispatch({
            type: SIGNUP_SUCCESS,
            payload: response.data
        });

    } catch (err) {

        dispatch({
            type: SIGNUP_FAIL
        })

    }
};

export const verify = (uid, token) => async dispatch => {

    const body = JSON.stringify({ uid, token });

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {

        await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/auth/users/activation/`, body, config);

        dispatch({
            type: ACTIVATION_SUCCESS,
        });

    } catch (err) {

        dispatch({
            type: ACTIVATION_FAIL
        })

    }
};

export const reset_password = (email) => async dispatch => {

    const body = JSON.stringify({ email });

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {

        await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/auth/users/reset_password/`, body, config);

        dispatch({
            type: PASSWORD_RESET_SUCCESS
        });

    } catch (err) {

        dispatch({
            type: PASSWORD_RESET_FAIL
        });

    }
};

export const reset_password_confirm = (uid, token, new_password) => async dispatch => {

    const body = JSON.stringify({ uid, token, new_password });

    const config = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    try {

        await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/auth/users/reset_password_confirm/`, body, config);

        dispatch({
            type: PASSWORD_RESET_CONFIRM_SUCCESS
        });

    } catch (err) {

        dispatch({
            type: PASSWORD_RESET_CONFIRM_FAIL
        });

    }
};

export const logout = () => dispatch => {

    dispatch({
        type: LOGOUT
    });

};