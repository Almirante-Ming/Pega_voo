export const name = (value: string) => {
    const regex = /^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$/
    return regex.test(value) || value === '';
  };
  