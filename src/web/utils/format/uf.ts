export const uf = (uf: string): string => {
  let sanitizedUf = uf.replace(/[^a-zA-Z]/g, '');
  
  if (sanitizedUf.length > 2) {
    sanitizedUf = sanitizedUf.substring(0, 2);
  }
  
  return sanitizedUf.toUpperCase();
};
