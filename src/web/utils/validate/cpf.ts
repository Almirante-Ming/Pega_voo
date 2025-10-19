export const cpf = (cpf: string): boolean => {
    // remover caracteres especiais
    cpf = cpf.replace(/[^\d]+/g, "");
  
    // verificar se o cpf possui 11 dígitos
    if (cpf.length !== 11) {
      return false;
    }
  
    // verificar se todos os dígitos são iguais
    if (new Set(cpf.split("")).size === 1) {
      return false;
    }
  
    // calcular o primeiro dígito verificador
    let sum = 0;
    for (let i = 0; i < 9; i++) {
      sum += parseInt(cpf[i]) * (10 - i);
    }
  
    let firstDigit = 11 - (sum % 11);
    if (firstDigit === 10 || firstDigit === 11) {
      firstDigit = 0;
    }
  
    // comparar o primeiro dígito verificador calculado com o informado
    if (firstDigit !== parseInt(cpf[9])) {
      return false;
    }
  
    // calcular o segundo dígito verificador
    sum = 0;
    for (let i = 0; i < 10; i++) {
      sum += parseInt(cpf[i]) * (11 - i);
    }
  
    let secondDigit = 11 - (sum % 11);
    if (secondDigit === 10 || secondDigit === 11) {
      secondDigit = 0;
    }
  
    // comparar o segundo dígito verificador calculado com o informado
    if (secondDigit !== parseInt(cpf[10])) {
      return false;
    }
  
    // retornar true se os dígitos verificadores são válidos
    return true;
  };
  