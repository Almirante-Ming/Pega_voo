import { fields } from "./fields";
import { field } from "./field";
import { cpf } from "./cpf";
import { cpfCnpj } from "./cpfCnpj";
import { creditCard } from "./creditCard";
import { isValidDateOfBirth } from "./isValidDateOfBirth";
import { sex } from "./sex";
import { completeName } from "./completeName"
import { name } from "./name";
import { creditCardName } from "./creditCardName";
import { isAdult } from "./isAdult";
import { isValidAge } from "./isValidAge";
import { isValidYear } from "./isValidYear";
import { completeSocialName } from "./completeSocialName"
import { dateCreditCard } from "./dateCreditCard"
import { cvvCreditCard } from "./cvvCreditCard"


export const validate = {
  fields,
  field,
  cpf,
  cpfCnpj,
  creditCard,
  creditCardName,
  isValidDateOfBirth,
  sex,
  name,
  completeName,
  isAdult,
  isValidAge,
  isValidYear,
  completeSocialName,
  dateCreditCard,
  cvvCreditCard
};
