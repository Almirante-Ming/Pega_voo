export const cnpj = (cnpj: string) => {  
  cnpj = cnpj?.replace(/[^0-9]+/g, "");

  cnpj = cnpj.substring(0, 14);

  if (cnpj.length <= 2) {
    return cnpj;
  } else if (cnpj.length <= 5) {
    return cnpj.replace(/(\d{2})(\d{0,3})/, "$1.$2");
  } else if (cnpj.length <= 8) {
    return cnpj.replace(/(\d{2})(\d{3})(\d{0,3})/, "$1.$2.$3");
  } else if (cnpj.length <= 12) {
    return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{0,4})/, "$1.$2.$3/$4");
  } else {
    return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{0,2})/, "$1.$2.$3/$4-$5");
  }
};
