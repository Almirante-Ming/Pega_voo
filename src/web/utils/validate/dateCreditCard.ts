export const dateCreditCard = (value: string) => {
    // value = value.replace(/[^0-9]/g, "");
    const data = value.split('/');
    let anoAtual = new Date().getFullYear();
    
    const dia = Number(data[0]);
    const ano = Number(data[1]);

    if(!ano) return false;

    if(dia > 31 || dia < 1 || ano < anoAtual) return false;

    return true;
  };
  