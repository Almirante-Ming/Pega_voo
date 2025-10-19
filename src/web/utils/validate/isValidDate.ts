import dayjs from "dayjs";
import customParseFormat from "dayjs/plugin/customParseFormat";

dayjs.extend(customParseFormat);

export const isValidDate = (value: string) => {
  const date = dayjs(value, "YYYY-MM-DD", true);
  const isValidDate = date.isValid();

  if (!isValidDate) {
    return false;
  }

  const currentYear = dayjs().year();
  const year = date.year();

  const isWithinRange = year >= currentYear - 130 && year <= currentYear + 130;

  return isWithinRange;
};
