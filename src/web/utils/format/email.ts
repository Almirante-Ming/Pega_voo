export const email = (email: string) => {
    email = email?.replace(/\s+/g, "");

    return email;
};
