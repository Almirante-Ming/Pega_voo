import { DateTime } from 'luxon';

export const timestamp = (isoString) => {
    const date = DateTime.fromISO(isoString);
    
    const formattedDate = date.toFormat("dd/MM/yyyy HH:mm");

    return formattedDate;
};
