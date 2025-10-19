export type ModelType = "static" | "dynamic" | "static-list" | "dynamic-list";

export type TipoDeDado = "string" | "number" | "boolean" | null;

export type TipoDeInput = "string" | "number" | "select" | "data" | "cpf" | "telefone" | "email" | "senha" | "fileUpload" | "timestamp";

export type Validacao = "dateOfBirth" | "cpf" | "telefone" | "email" | "senha" | "data";

export interface ModelItem {
    chave: string | number;
    descricao: string;
}

export interface Campo {
    label: string;
    propriedade: string;
    tipoDeInput: TipoDeInput;
    obrigatorio?: boolean;
    tipoDeDado?: TipoDeDado;
    placeholder?: string;
    validacao?: Validacao;
    modelType?: ModelType;
    model?: ModelItem[];
    valoresNegativos?: boolean;
    maxLength?: number;
    valorPadrao?: any;
    habilitado?: boolean;
    icone?: string;
    query?: string;
    mostrarHora?: boolean
}

export interface GrupoFormulario {
    title?: string;
    columns: Campo[];
}

export type Formulario = GrupoFormulario[];