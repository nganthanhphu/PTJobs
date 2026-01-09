import axios from "axios";

const HOST = "http://10.0.2.2:8000";

export const endpoints = {
    register: "/users/",
    "current-user": "/users/current-user/",
    login: "/o/token/",

    "job-categories": "/job-categories/",

    jobposts: "/jobposts/",
    "jobpost-details": (id) => `/jobposts/${id}/`,

    applications: "/applications/",
    "application-details": (id) => `/applications/${id}/`,
    "application-reviews": (id) => `/applications/${id}/reviews/`,

    "candidate-details": (id) => `/candidates/${id}/`,
    "candidate-reviews": (id) => `/candidates/${id}/reviews/`,

    "company-details": (id) => `/companies/${id}/`,
    "company-reviews": (id) => `/companies/${id}/reviews/`,

    "company-images": "/company-images/",
    "company-image-details": (id) => `/company-images/${id}/`,

    following: "/following/",
    "following-details": (id) => `/following/${id}/`,

    resumes: "/resumes/",
    "resume-details": (id) => `/resumes/${id}/`,

    "review-details": (id) => `/reviews/${id}/`,
};

/**
 * @param {string}
 */
export const authApis = (token) => {
    return axios.create({
        baseURL: HOST,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
};

export default axios.create({
    baseURL: HOST,
});
