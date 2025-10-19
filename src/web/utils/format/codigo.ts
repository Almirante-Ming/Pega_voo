export const codigo = (codigo: string) => {
    const newCodigo = codigo?.replace(/[^A-Za-z0-9]/g, "");

    return newCodigo;
}