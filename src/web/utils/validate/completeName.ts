export const completeName = (value: string) => {
    const fullName = value.replace(/\s\s+/g, ' ').split(' ');
    const surname = fullName[1] ?? "";

    return fullName.length > 1 && surname.length >= 1;
};
