export const data = (data: string) => {
  data = data.replace(/[^0-9]+/g, "");
  
  if (data.length > 8) {
    data = data.substring(0, 8);
  }

  if (data.length > 4) {
    data = data.replace(/(\d{2})(\d{2})(\d{1,4})/, "$1/$2/$3");
  } else if (data.length > 2) {
    data = data.replace(/(\d{2})(\d{1,2})/, "$1/$2");
  }

  return data;
};
