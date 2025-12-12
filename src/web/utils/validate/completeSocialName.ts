export const completeSocialName = (value: string) => {
    const fullName = value.replace(/\s\s+/g, ' ').split(' ');

    if(fullName[0] !== ''){        
        return fullName[0].length > 1;
    }else{
        return true
    }
  };