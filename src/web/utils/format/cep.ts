export const cep = (cep: string): string => {
  cep = cep?.replace(/[^0-9]/g, "");

  if (cep.length > 8) {
    cep = cep.substring(0, 8);
  }

  if (cep.length > 5) {
    cep = cep.replace(/(\d{5})(\d{1,3})/, "$1-$2");
  }

  return cep;
};
  