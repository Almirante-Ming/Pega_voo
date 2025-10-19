import { cnpj } from "./cnpj";
import { cpf } from "./cpf";

export function cpfcnpj(value: string): string {
  value = value.replace(/[^0-9]+/g, "");

  if (value.length <= 11) {
    return cpf(value);
  } else {
    return cnpj(value);
  }
}
