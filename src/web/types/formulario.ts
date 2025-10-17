export type ModelType = "static" | "dynamic" | "static-list" | "dynamic-list";

export type TipoDeDado = "string" | "number" | "boolean";

export type TipoDeInput = "string" | "number" | "select" | "data" | "cpf" | "telefone" | "email" | "senha" | "fileUpload";

export interface ModelItem {
    chave: string | number;
    descricao: string;
}

export interface Campo {
    label: string;
    tipoDeDado: TipoDeDado;
    propriedade: string;
    tipoDeInput: TipoDeInput;
    obrigatorio: boolean;
    placeholder?: string;
    validation?: string;
    modelType?: ModelType;
    model?: ModelItem[];
    valoresNegativos?: boolean;
    maxLength?: number;
    valorPadrao?: any;
    habilitado?: boolean;
    icone?: string;
    query?: string;
    firstOption?: any;
}

export interface GrupoFormulario {
    title?: string;
    columns: Campo[];
}

export type Formulario = GrupoFormulario[];