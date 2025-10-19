import { z } from "zod";
import { validate } from "@/utils";
import { ErrorMessagesEnum } from "@/constants";

export default {
  sex: z.object({
    sex: z
      .string({
        required_error: ErrorMessagesEnum["INVALID_SEX"],
        invalid_type_error: ErrorMessagesEnum["INVALID_SEX"],
      })
      .refine((value) => validate.sex(value), {
        path: ["sex"],
        message: ErrorMessagesEnum["INVALID_SEX"],
      }),
  }),
  sexo: z.object({
    sexo: z
      .string({
        required_error: ErrorMessagesEnum["INVALID_SEX"],
        invalid_type_error: ErrorMessagesEnum["INVALID_SEX"],
      })
      .refine((value) => validate.sex(value), {
        path: ["sex"],
        message: ErrorMessagesEnum["INVALID_SEX"],
      }),
  }),

  email: z.object({
    email: z
      .string()
      .trim()
      .email({ message: ErrorMessagesEnum["INVALID_EMAIL"] }),
  }),
  cpf: z.object({
    cpf: z
      .string()
      .length(11, { message: ErrorMessagesEnum["MIN_LENGTH_CPF"] })
      .refine((value) => validate.cpf(value), {
        path: ["cpf"],
        message: ErrorMessagesEnum["INVALID_CPF"],
      }),
  }),
  cpfCnpj: z.object({
    cpfCnpj: z
      .string()
      .min(11, { message: ErrorMessagesEnum["INVALID_CPF_CNPJ"] })
      .max(18, { message: ErrorMessagesEnum["INVALID_CPF_CNPJ"] })
      .refine((value) => validate.cpfCnpj(value), {
        path: ["cpfCnpj"],
        message: ErrorMessagesEnum["INVALID_CPF_CNPJ"],
      }),
  }),
  cpfcnpj: z.object({
    cpfcnpj: z
      .string()
      .min(11, { message: ErrorMessagesEnum["INVALID_CPF_CNPJ"] })
      .max(18, { message: ErrorMessagesEnum["INVALID_CPF_CNPJ"] })
      .refine((value) => validate.cpfCnpj(value), {
        path: ["cpfCnpj"],
        message: ErrorMessagesEnum["INVALID_CPF_CNPJ"],
      }),
  }),
  phone: z.object({
    phone: z
      .string()
      .min(10, { message: ErrorMessagesEnum["INVALID_PHONE"] })
      .max(15, { message: ErrorMessagesEnum["INVALID_PHONE"] }),
  }),
  telefone: z.object({
    telefone: z
      .string()
      .min(10, { message: ErrorMessagesEnum["INVALID_PHONE"] })
      .max(15, { message: ErrorMessagesEnum["INVALID_PHONE"] }),
  }),
  creditCardName: z.object({
    name: z.string().refine((value) => validate.name(value), {
      path: ["name"],
      message: ErrorMessagesEnum["INVALID_CREDIT_CARD_NAME"],
    }),
  }),
  name: z.object({
    name: z
      .string()
      .trim()
      .refine((value: string) => validate.name(value), {
        path: ["name"],
        message: ErrorMessagesEnum["INVALID_NAME"],
      })
      .refine((value: string) => validate.completeName(value), {
        path: ["completeName"],
        message: ErrorMessagesEnum["INCOMPLETE_NAME"],
      }),
  }),
  nome: z.object({
    nome: z
      .string()
      .trim()
      .refine((value: string) => validate.name(value), {
        path: ["name"],
        message: ErrorMessagesEnum["INVALID_NAME"],
      })
      .refine((value: string) => validate.completeName(value), {
        path: ["completeName"],
        message: ErrorMessagesEnum["INCOMPLETE_NAME"],
      }),
  }),
  socialName: z.object({
    socialName: z
      .string()
      .trim()
      .refine((value: string) => validate.name(value), {
        path: ["name"],
        message: ErrorMessagesEnum["INVALID_NAME"],
      })
      .refine((value: string) => validate.completeSocialName(value), {
        path: ["completeSocialName"],
        message: ErrorMessagesEnum["INCOMPLETE_NAME"],
      }),
  }),
  zipCode: z.object({
    zipCode: z
      .string()
      .min(8, { message: ErrorMessagesEnum["INVALID_ZIP_CODE"] }),
  }),
  cep: z.object({
    cep: z.string().min(8, { message: ErrorMessagesEnum["INVALID_ZIP_CODE"] }),
  }),
  street: z.object({
    street: z.string().min(1, ErrorMessagesEnum["INVALID_STREET"]),
  }),
  logradouro: z.object({
    logradouro: z.string().min(1, ErrorMessagesEnum["INVALID_STREET"]),
  }),
  addressNumber: z.object({
    addressNumber: z
      .string()
      .min(1, ErrorMessagesEnum["INVALID_ADDRESS_NUMBER"]),
  }),
  numero: z.object({
    numero: z.string().min(1, ErrorMessagesEnum["INVALID_ADDRESS_NUMBER"]),
  }),
  city: z.object({
    city: z.string().min(1, ErrorMessagesEnum["INVALID_CITY"]),
  }),
  cidade: z.object({
    cidade: z.string().min(1, ErrorMessagesEnum["INVALID_CITY"]),
  }),
  neighborhood: z.object({
    neighborhood: z.string().min(1, ErrorMessagesEnum["INVALID_NEIGHBORHOOD"]),
  }),
  bairro: z.object({
    bairro: z.string().min(1, ErrorMessagesEnum["INVALID_NEIGHBORHOOD"]),
  }),
  uf: z.object({
    uf: z.string().length(2, ErrorMessagesEnum["INVALID_UF"]),
  }),
  password: z.object({
    password: z.string().min(8, ErrorMessagesEnum.INVALID_PASSWORD),
  }),
  senha: z.object({
    senha: z.string().min(8, ErrorMessagesEnum.INVALID_PASSWORD),
  }),
  creditCard: z.object({
    creditCard: z.string().refine((value) => validate.creditCard(value), {
      path: ["creditCard"],
      message: ErrorMessagesEnum["INVALID_CREDIT_CARD_NUMBER"],
    }),
  }),
  creditCardNumber: z.object({
    creditCardNumber: z
      .string()
      .min(14, ErrorMessagesEnum.INVALID_CREDIT_CARD_NUMBER)
      .refine((value) => validate.creditCard(value), {
        path: ["creditCardNumber"],
        message: ErrorMessagesEnum["INVALID_CREDIT_CARD_NUMBER"],
      }),
  }),
  dateCreditCard: z.object({
    dateCreditCard: z
      .string()
      .refine((value) => validate.dateCreditCard(value), {
        path: ["dateCreditCard"],
        message: ErrorMessagesEnum["INVALID_CREDIT_CARD_DATE"],
      }),
  }),
  creditCardExpirationDate: z.object({
    creditCardExpirationDate: z
      .string()
      .min(5, ErrorMessagesEnum.INVALID_CREDIT_CARD_EXPIRATION_DATE),
  }),
  cvvCreditCard: z.object({
    cvvCreditCard: z
      .string()
      .length(3, ErrorMessagesEnum["INVALID_CVV_DATE"])
      .refine((value) => validate.cvvCreditCard(value), {
        path: ["cvvCreditCard"],
        message: ErrorMessagesEnum["INVALID_CVV_DATE"],
      }),
  }),
  data: z.object({
    data: z
      .string()
      .min(10, ErrorMessagesEnum.INVALID_DATE)
      .superRefine((value, ctx) => {
        if (!validate.isValidDate(value)) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ["isValidDate"],
            message: ErrorMessagesEnum["INVALID_DATE"],
          });
        }
      }),
  }),
  date: z.object({
    date: z
      .string()
      .min(10, ErrorMessagesEnum.INVALID_DATE)
      .superRefine((value, ctx) => {
        if (!validate.isValidDate(value)) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ["isValidDate"],
            message: ErrorMessagesEnum["INVALID_DATE"],
          });
        }
      }),
  }),
  dateOfBirth: z.object({
    dateOfBirth: z
      .string()
      .min(10, ErrorMessagesEnum.INVALID_DATE_OF_BIRTH)
      .superRefine((value, ctx) => {
        if (!validate.isValidDateOfBirth(value)) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ["isValidDateOfBirth"],
            message: ErrorMessagesEnum["INVALID_DATE_OF_BIRTH"],
          });
        }
        if (!validate.isValidYear(value)) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ["isValidYear"],
            message: ErrorMessagesEnum["INVALID_DATE_OF_BIRTH"],
          });
        }
      }),
  }),
  data_nascimento: z.object({
    data_nascimento: z
      .string()
      .min(10, ErrorMessagesEnum.INVALID_DATE_OF_BIRTH)
      .superRefine((value, ctx) => {
        if (!validate.isValidDateOfBirth(value)) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ["isValidDateOfBirth"],
            message: ErrorMessagesEnum["INVALID_DATE_OF_BIRTH"],
          });
        }
        if (!validate.isValidYear(value)) {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ["isValidYear"],
            message: ErrorMessagesEnum["INVALID_DATE_OF_BIRTH"],
          });
        }
      }),
  }),
  confirmationEmail: z
    .object({
      email: z
        .string()
        .trim()
        .email({ message: ErrorMessagesEnum["INVALID_EMAIL"] }),
      emailConfirmation: z
        .string()
        .trim()
        .email({ message: ErrorMessagesEnum["INVALID_EMAIL"] }),
    })
    .refine((data) => data.email === data.emailConfirmation, {
      message: "Emails Diferentes",
    }),
  compareConfirmationEmail: z
    .object({
      email: z.string(),
      emailConfirmation: z
        .string()
        .email({ message: ErrorMessagesEnum["INVALID_EMAIL"] }),
    })
    .superRefine((value, ctx) => {
      if (value.email !== value.emailConfirmation) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ["emailConfirmation"],
          message: ErrorMessagesEnum["EMAILS_DO_NOT_MATCH"],
        });
      }
    }),
};
