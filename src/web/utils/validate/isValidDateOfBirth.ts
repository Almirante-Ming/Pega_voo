import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";

dayjs.extend(customParseFormat);

export const isValidDateOfBirth = (value: string) => {
  const date = dayjs(value, "YYYY-MM-DD", true);
  const isValidDate = date.isValid();

  if (!isValidDate) {
    return false;
  }

  const currentYear = dayjs().year();
  const year = date.year();

  const isWithinRange = year >= currentYear - 100 && year <= currentYear + 30;

  return isWithinRange;
};
