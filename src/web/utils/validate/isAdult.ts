import dayjs from "dayjs";

dayjs.locale("pt-br");

export const isAdult = (value: string): boolean => {
  const currentDate = dayjs();
  const birthDate = dayjs(value, "YYYY-MM-DD");
  const age = currentDate.diff(birthDate, "year");
  return age >= 16;
};
