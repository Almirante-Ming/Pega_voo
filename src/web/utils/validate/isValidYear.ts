import dayjs from "dayjs";

dayjs.locale("pt-br");

export const isValidYear = (value: string): boolean => {
  const currentYear = dayjs().year();
  const inputYear = dayjs(value, "YYYY-MM-DD").year();

  return inputYear <= currentYear;
};
