import { cpf } from "./cpf";
import { cnpj } from "./cnpj";
import { cpfcnpj } from "./cpfcnpj";
import { telefone } from "./telefone";
import { cep } from "./cep";
import { uf } from "./uf";
import { data } from "./data";
import { timestamp } from "./timestamp";
import { numberString } from "./numberString";
import { int } from "./int";
import { codigo } from "./codigo";
import { email } from "./email";
import { tag } from "./tag";

export const format = {
  cpf,
  cnpj,
  cpfcnpj,
  telefone,
  cep,
  uf,
  data,
  timestamp,
  numberString,
  int,
  codigo,
  email,
  tag
};

export type Masks = keyof typeof format;
