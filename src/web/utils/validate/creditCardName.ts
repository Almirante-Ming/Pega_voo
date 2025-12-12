export const creditCardName = (creditCardName: string) => {
    creditCardName = creditCardName?.replace(
      /[^A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$/g,
      ""
    );
  
    return creditCardName.toUpperCase();
  };
  