export const telefone = (telefone: string) => {
  telefone = telefone?.replace(/[^0-9]/g, "");
  
  if (telefone.length > 11) {
    telefone = telefone.substring(0, 11);
  }

  if (telefone.length === 10) {
    return telefone.replace(/(\d{2})(\d{4})(\d{4})/, "($1) $2-$3");
  } else if (telefone.length === 11) {
    return telefone.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
  }

  return telefone;
};
