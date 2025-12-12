export const cpf = (cpf: string) => {
	var num = cpf.replace(/[^\d]/g, "");
	var len = num.length;
  
	if (len > 11) {
	  num = num.substring(0, 11);
	}
  
	if (len <= 6) {
	  cpf = num.replace(/(\d{3})(\d{1,3})/g, "$1.$2");
	} else if (len <= 9) {
	  cpf = num.replace(/(\d{3})(\d{3})(\d{1,3})/g, "$1.$2.$3");
	} else {
	  cpf = num.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/g, "$1.$2.$3-$4");
	}
	
	return cpf;
  };
  