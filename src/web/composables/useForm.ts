import schemas from "@/utils/validate/schemas";

import { validate } from "../utils"

interface FormFields {
  [field: string]: string;
}

interface Form {
  form: FormFields;
  errors: FormFields;
}

export const useForm = (fields: string[], optionalFields: string[]) => {
  const formIsValid = ref(false);

  const state = reactive<Form>({
    form: {},
    errors: {}
  });

  onBeforeMount(() => {

    fields.forEach((field) => {
      state.form[field] = "";
      state.errors[field] = "";
    });
  });

  function handleValidateField(field: string, validationType?: string) {
    const schemaKey = validationType || field;
    let fieldToValidate: string = "";

    for (const schema in schemas) {      
      if (schema == schemaKey) {        
        fieldToValidate = state.form[field];
        if (!schema) return;
        if (["zipCode", "phone", "cpf", "cnpj"].includes(schema)) fieldToValidate = fieldToValidate.replace(/[^0-9]/g, "");
      }

      if (field === "emailConfirmation") {
        const { error } = validate.field(schemas[schemaKey] as any, {
          email: state.form.email,
          [field]: fieldToValidate
        });

        state.errors[field] = error;
      } else {
        if (!schemas[schemaKey] && fields.includes(field) && state.form[field]?.length === 0) {
          state.errors[field] = "Campo obrigatório";
          return;
        }

        if (optionalFields.includes(field) && state.form[field]?.length === 0) {
          state.errors[field] = "";
          return;
        }

        const { error } = validate.field(schemas[schemaKey] as any, {
          [schemaKey]: fieldToValidate
        });
        state.errors[field] = error;
      }
    }
  }

  function handleValidateFields(fieldToValidationMap?: Record<string, string>) {
    let fields: string[] = Object.keys(state.form) as string[];

    fields = fields.filter((field) => {
      return field !== "complement" && field !== "ibgeCode";
    });

    fields.forEach((field) => {
      const validationType = fieldToValidationMap?.[field];
      handleValidateField(field, validationType);
    });
  }

  watch(
    () => state,
    (state) => {
      const thereIsNoErrors = Object.values(state.errors).every(
        (error) => !error
      );

      const formWithoutOptionals = { ...state.form };
      optionalFields.forEach(field => {
        if (!formWithoutOptionals[field]?.length)
          delete formWithoutOptionals[field];
      });

      const thereIsNoEmptyFields = Object.values(formWithoutOptionals).every(
        (value: any) => {
          if (value === null || value === undefined) {
            return false;
          }
      
          if (typeof value === 'object') {
            if (value?.chave !== undefined && value?.chave !== null && value?.chave !== '') {
              return true;
            }
      
            return value?.toString()?.length > 0;
          }
      
         if (typeof value === 'string' || Array.isArray(value)) {
            return value.length > 0;
          }

          if (typeof value === 'boolean') {
            return true;
          }
      
          if (typeof value === 'number') {
            return true;
          }
      
          return !!value;
        }
      );
            
      if (thereIsNoErrors && thereIsNoEmptyFields) {
        // true se não houver erros
        formIsValid.value = true;
      } else if (!thereIsNoErrors || !thereIsNoEmptyFields) {
        // false se houver erros
        formIsValid.value = false;
      }
    },
    {
      deep: true
    }
  );

  return {
    formIsValid,
    ...toRefs(state),
    handleValidateField,
    handleValidateFields
  };
};