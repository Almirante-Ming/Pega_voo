export function atualizarFormulario(
  form: any,
  validarCampo: (field: string, validacao?: string) => void
) {
  return function atualizarFormulario(field: string, value: any, validar?: string) {
    form.value[field] = value?.target?.value
      ? value.target.value
      : typeof value === "boolean"
      ? value
      : typeof value === "string" || typeof value === "number"
      ? value
      : value?.chave ?? ""
    
    // Executa validação se especificada
    
    if (validar) {        
      validarCampo(field, validar);
    } else {
      validarCampo(field);
    }
  }
}
