import { cpf } from "./cpf";
import { cnpj } from "./cnpj";

export const cpfCnpj = (cpfCnpj: string): boolean => {
  if (cpfCnpj.length === 11) {
    return cpf(cpfCnpj);
  } else if (cpfCnpj.length === 14) {
    return cnpj(cpfCnpj);
  } else {
    return false;
  }
};
