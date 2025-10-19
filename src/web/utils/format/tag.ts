export function tag(value: string): string {
  return value
    .replace(/\s+/g, '-')          // Substitui espaços por traços
    .replace(/[^a-zA-Z0-9-]/g, '') // Remove tudo que não for letra, número ou traço
    .replace(/-+/g, '-')           // Normaliza múltiplos traços consecutivos em um único traço
    .toLowerCase();                // Converte tudo para minúsculo
}
