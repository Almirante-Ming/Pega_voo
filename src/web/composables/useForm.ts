import schemas from "@/utils/validate/schemas";

import { validate } from "../utils"

interface FormFields {
  [field: string]: string;
}

interface Form {
  form: FormFields;
  erros: FormFields;
}

export const useForm = (fields: string[], optionalFields: string[]) => {
  const formValido = ref(false);

  const state = reactive<Form>({
    form: {},
    erros: {}
  });

  onBeforeMount(() => {

    fields.forEach((field) => {
      state.form[field] = "";
      state.erros[field] = "";
    });
  });

  function validarCampo(field: string, validationType?: string) {
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

        state.erros[field] = error;
      } else {
        if (!schemas[schemaKey] && fields.includes(field) && state.form[field]?.length === 0) {
          state.erros[field] = "Campo obrigatório";
          return;
        }

        if (optionalFields.includes(field) && state.form[field]?.length === 0) {
          state.erros[field] = "";
          return;
        }

        const { error } = validate.field(schemas[schemaKey] as any, {
          [schemaKey]: fieldToValidate
        });
        state.erros[field] = error;
      }
    }
  }

  function validarFormulario(fieldToValidationMap?: Record<string, string>) {
    let fields: string[] = Object.keys(state.form) as string[];

    fields = fields.filter((field) => {
      return field !== "complement" && field !== "ibgeCode";
    });

    fields.forEach((field) => {
      const validationType = fieldToValidationMap?.[field];
      validarCampo(field, validationType);
    });
  }

  watch(
    () => state,
    (state) => {
      const thereIsNoErrors = Object.values(state.erros).every(
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
        formValido.value = true;
      } else if (!thereIsNoErrors || !thereIsNoEmptyFields) {
        // false se houver erros
        formValido.value = false;
      }
    },
    {
      deep: true
    }
  );

  return {
    formValido,
    ...toRefs(state),
    validarCampo,
    validarFormulario
  };
};